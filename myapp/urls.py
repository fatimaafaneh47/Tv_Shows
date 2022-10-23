from django.urls import path     
from . import views
urlpatterns = [
    path('',views.main_page),
    path('register',views.registration),
    path('login',views.login),
    path('logout',views.logout),
    path('shows',views.success),
    path('shows/new',views.add_page),
    path('shows/add',views.add_show),
    path('shows/<int:id>',views.show_details_page),
    path('shows/edit/<int:id>',views.Update_page),
    path('shows/update/<int:id>',views.update),
    path('shows/delete/<int:id>',views.delete)
]