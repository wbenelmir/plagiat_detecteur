from django.urls import path
from . import views

urlpatterns = [
    path('<str:code_data>', views.analyse , name='analyse'), 
]