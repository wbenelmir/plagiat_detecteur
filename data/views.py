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

from .analyse import *
from django.conf import settings

# if settings.DEBUG:
#     print(str(settings.MEDIA_URL)+ '/'+datasource.doc.name)
# else:
#     print(str(settings.MEDIA_ROOT)+ '/'+datasource.doc.name)
src = str(settings.MEDIA_URL) 
src =  'media'

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
                
                file_name = str(datasource.doc.name)
                list = file_name.split('.')
                file_name = list[0]
                discriptor = Segmentation(src, file_name)
                
                if datasource and discriptor:
                    datasource.codes_pages_de_garde = discriptor[0]['codes_pages_de_garde'][0]#.replace('  ','')
                    datasource.titres_pages_de_garde = discriptor[0]['titres_pages_de_garde'][0]#.replace(': SIOD ', '')
                    datasource.liens_descripteurs_locaux_type = discriptor[0]['liens_descripteurs_locaux'][0]['type']
                    datasource.nombre_paragraphe = discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_paragraphe']
                    datasource.nombre_phrase = discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_phrase']
                    datasource.nombre_mot = discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_mot']
                    if request.user.is_superuser:
                        datasource.is_archive = True
                    else:
                        datasource.is_archive = False
                        
                    datasource.save()

                    # print(discriptor[0]['codes_pages_de_garde'][0])
                    # print(discriptor[0]['titres_pages_de_garde'][0])
                    # print(discriptor[0]['liens_descripteurs_locaux'][0]['type'])
                    # print(discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_paragraphe'])
                    # print(discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_phrase'])
                    # print(discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_mot'])

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