from unittest import defaultTestLoader
from django.db import models
from distutils.log import error
from typing import Text
from django.db import models
import re 
from django.core.validators import validate_email

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors={}
        if len(post_data['first_name'])<1:
            errors['first_name']='please enter youre first name'
        if len(post_data['last_name'])<1:
            errors['last_name']='please enter youre last name'
        if len(post_data['first_name'])<2:
            errors['first_name']='first name should be at least 2 chcechtors'
        if len(post_data['last_name'])<2:
            errors['last_name']='first name should be at least 2 chcechtors'
        if len(post_data['password'])<2:
            errors['password']='first name should be at least 8 chcechtors'
        try: 
             validate_email(post_data['email'])
        except:
             errors['email']='please enter a valid email'
        if len(post_data['password'])<1:
            errors['password']='please enter a password'
        if post_data['password'] !=post_data['confirm_pw']:
            errors['confirm_pw'] ='youre password didnt match'
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    confirm_pw = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class ShowManager(models.Manager):
    
    def show_validator(self, posted_data):
        errors = {}
        if len(posted_data['title']) < 3:
            errors['title'] = "title must be at least 3 characters length!"
        if len(posted_data['network']) < 3:
            errors['network'] = "network must be at least 3 characters length!"
        if len(posted_data['description']) < 3:
            errors['description'] = "description must be at least 3 characters length!"  
        if len(posted_data['title']) < 1:
            errors['title'] = "title must be enterd" 
        if len(posted_data['network']) < 1:
            errors['network'] = "network must be enterd" 
        if len(posted_data['description']) < 1:
            errors['description'] = "description must be enterd"  
        if len(posted_data['releasedate']) < 1:
            errors['releasedate'] = "Release_Date must be enterd"  
        return errors
        
        

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField() 
    desc = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    watched_by = models.ForeignKey(User, related_name="shows", on_delete = models.CASCADE) 
    objects = ShowManager() 
    