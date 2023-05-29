from django.urls import path
from . import views

urlpatterns = [
    path('show', views.datasources , name='datasources'), 
    path('add', views.add_datasource , name='add_datasource'), 
    path('edit/<str:code>', views.edit_datasource , name='edit_datasource'), 
]