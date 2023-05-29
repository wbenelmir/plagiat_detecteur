from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from authentification.decorators import *

@login_required(login_url='login')
def datasources(request):

    datasources = Datasource.objects.all().order_by('id')

    context = {
        'datasources' : datasources,
    }
    return render(request, 'dataSource/show.html', context)

@login_required(login_url='login')
def add_datasource(request):

    try:
        user = User.objects.get(username = request.user)
    except:
        user = None

    datasourceForm = DatasourceForm()
    if request.method == 'POST':
        datasourceForm = DatasourceForm(request.POST, request.FILES)
        # check whether it's valid:
        if datasourceForm.is_valid():
            datasourceForm.save()
            try:
                datasource = Datasource.objects.get(code_data=request.POST.get('code_data'))
                if user:
                    datasource.user = user
                    datasource.save()
            except BaseException as e:
                print(str(e))
            messages.success(request, 'Les données ont été insérées avec succès.')
        else:
            messages.error(request,'Une erreur s\'est produite lors de l\'insertiondes données')
            print(datasourceForm.errors)

    context = {
        'datasourceForm' : datasourceForm,
        'user' : user,
    }
    return render(request, 'dataSource/add.html', context)

@login_required(login_url='login')
def edit_datasource(request, code):
    try:
        user = User.objects.get(username = request.user)
    except:
        user = None

    try:
        datasource = Datasource.objects.get(code_data = code)
    except:
        return redirect('datasources')

    datasourceForm = DatasourceForm(instance=datasource)
    if request.method == 'POST':
        datasourceForm = DatasourceForm(request.POST, request.FILES, instance=datasource)
        # check whether it's valid:
        if datasourceForm.is_valid():
            datasourceForm.save()
            try:
                datasource = Datasource.objects.get(code_data=request.POST.get('code_data'))
                if user:
                    datasource.user = user
                    datasource.save()
                    redirect('../../../datasource/edit/' + datasource.code_data)
            except BaseException as e:
                print(str(e))
            messages.success(request, 'Les données ont été modifié avec succès.')
        else:
            messages.error(request,'Une erreur s\'est produite lors de la modification des données')
            print(datasourceForm.errors)

    context = {
        'datasourceForm' : datasourceForm,
        'user' : user,
        'doc_path' : datasource.doc
    }
    return render(request, 'dataSource/edit.html', context)