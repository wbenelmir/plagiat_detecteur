from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage , name='login'), 
    path('logout', views.logoutuser , name='logout'), 
    path('register', views.register , name='register'), 
]