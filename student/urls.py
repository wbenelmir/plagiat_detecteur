from django.urls import path
from . import views

urlpatterns = [
    path('basicInfo', views.basicInfo , name='basicInfo'), 
    path('contactInfo', views.contactInfo , name='contactInfo'), 
    
    path('contact', views.user_contact, name='user_contact'),
]