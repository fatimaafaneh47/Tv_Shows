from audioop import add
import email
from email.message import Message
from multiprocessing import context
from os import remove
from re import S
from xml.etree.ElementTree import Comment
from django.forms import PasswordInput
from django.shortcuts import render ,redirect
from django.contrib import messages
import bcrypt

from myapp.models import Show, User


def main_page(request):
    return render(request,"index.html")

def success(request ):
    if "user_id" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context={
        'shows':Show.objects.all(),
        'this_user': User.objects.get(id = request.session['user_id']),
    }
    return render(request,"shows.html",context)

def registration(request):
    form =request.POST
    errors=User.objects.basic_validator(form)
    if len(errors)>0:
        for key , val in errors.items():
            messages.error(request,val)
        return redirect('/')
    user = User.objects.create(first_name=form['first_name'],last_name=form['last_name']
    ,email=form['email'],password=bcrypt.hashpw(form['password'].encode(),bcrypt.gensalt()).decode())
    request.session["user_id"]= user.id
    return redirect('/shows')

def login(request):
    form =request.POST
    try:
        user=User.objects.get(email=form['email'])
    except:
        messages.error(request,'check youre email and password!')
        return redirect('/')
    if bcrypt.checkpw(form['password'].encode(),user.password.encode()):
        request.session['user_id']= user.id
        request.session['first_name'] = user.first_name
        return redirect('/shows')
    messages.error(request,'check youre email and password!')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/') 

def add_page(request):
    return render(request,'add_page.html')

def add_show(request):
    form =request.POST
    errors=Show.objects.show_validator(form)
    if len(errors)>0:
        for key , val in errors.items():
            messages.error(request,val)
        return redirect('/shows/new')
    
    this_show=Show.objects.create(
        title = request.POST['title'],
        network=request.POST['network'],
        release_date = request.POST['releasedate'],
        desc=request.POST["description"],
        watched_by = User.objects.get(id=request.session.get('user_id')),
    )
    
    return redirect ('/shows')

def show_details_page(request,id):
    context = {
        "show": Show.objects.get(id=id),
    }
    return render(request,'show_details.html',context)

def Update_page(request,id):
    context = {
        "show": Show.objects.get(id=id),
    }
    return render(request,'edit_page.html',context)

def update(request,id):
    form =request.POST
    errors=Show.objects.show_validator(form)
    if len(errors)>0:
        for key , val in errors.items():
            messages.error(request,val)
        return redirect(f'/shows/edit/{id}')
    show= Show.objects.get(id=id)
    show.title=request.POST['title']
    show.network=request.POST['network']
    show.release_date=request.POST['releasedate']
    show.desc=request.POST['description']
    show.save()
    return redirect('/shows')

def delete(request ,id):
    show=Show.objects.get(id=id)
    show.delete()
    return redirect('/shows')