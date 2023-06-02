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

import os
import shutil
from django.conf import settings

# if settings.DEBUG:
#     print(str(settings.MEDIA_URL)+ '/'+datasource.doc.name)
# else:
#     print(str(settings.MEDIA_ROOT)+ '/'+datasource.doc.name)
src = str(settings.MEDIA_URL) 
src =  'media'

def copy_file(source_path, destination_path):
    # Get the full paths for the source and destination files
    source_full_path = os.path.join(settings.MEDIA_ROOT, source_path)
    destination_full_path = os.path.join(settings.MEDIA_ROOT, destination_path)

    # Create the destination directory if it doesn't exist
    os.makedirs(os.path.dirname(destination_full_path), exist_ok=True)

    # Copy the file from source to destination
    shutil.copy2(source_full_path, destination_full_path)

@login_required(login_url='login')
def datasources(request):

    if request.user.is_superuser:
        datasources = Datasource.objects.filter(is_archive = True)
    else:
        datasources = Datasource.objects.filter(is_archive = False)

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

                ### Segmentation ############################################################################################

                global_discriptor = []

                if request.user.is_superuser:
                    copy_file(datasource.doc.name, 'archive/'+datasource.doc.name)
                    convertir_en_texte('media/archive', file_name)
                    dictionnaire_nettoye = lire_fichiers_texte('media/archive', file_name)
                else:
                    convertir_en_texte('media', file_name)
                    dictionnaire_nettoye = lire_fichiers_texte('media', file_name)

                descripteur_global = extraire_pages_de_garde(dictionnaire_nettoye)
                descripteur_local_intro = extraire_conclusion(dictionnaire_nettoye, descripteur_global)
                descripteur_local_conclu = extraire_introduction(dictionnaire_nettoye, descripteur_global)
                global_discriptor.append(descripteur_global)

                # dictionnaire_nettoye = lire_fichiers_texte(src, file_name)

                # global_discriptor = []

                descripteur_global = extraire_pages_de_garde(dictionnaire_nettoye)
                descripteur_local_intro = extraire_conclusion(dictionnaire_nettoye, descripteur_global)
                descripteur_local_conclu = extraire_introduction(dictionnaire_nettoye, descripteur_global)
                global_discriptor.append(descripteur_global)

                if datasource and global_discriptor:
                    datasource.codes_pages_de_garde = global_discriptor[0]['codes_pages_de_garde'][0]#.replace('  ','')
                    datasource.titres_pages_de_garde = global_discriptor[0]['titres_pages_de_garde'][0]#.replace(': SIOD ', '')
                    datasource.pg_titre_nombre_paragraphe = global_discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_paragraphe']
                    datasource.pg_titre_nombre_phrase = global_discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_phrase']
                    datasource.pg_titre_nombre_mot = global_discriptor[0]['liens_descripteurs_locaux'][0]['lien']['nombre_mot']

                    if request.user.is_superuser:
                        datasource.is_archive = True
                    else:
                        datasource.is_archive = False
                    
                    datasource.descripteur_global = global_discriptor
                    datasource.save()

                if datasource and descripteur_local_intro:
                    datasource.conclusion_nombre_paragraphe = descripteur_local_intro['nombre_paragraphe']
                    datasource.conclusion_nombre_phrase = descripteur_local_intro['nombre_phrase']
                    datasource.conclusion_nombre_mot = descripteur_local_intro['nombre_mot']
                    
                    datasource.descripteur_conclusion = descripteur_local_intro
                    datasource.save()

                if datasource and descripteur_local_conclu:
                    datasource.introduction_nombre_paragraphe = descripteur_local_conclu['nombre_paragraphe']
                    datasource.introduction_nombre_phrase = descripteur_local_conclu['nombre_phrase']
                    datasource.introduction_nombre_mot = descripteur_local_conclu['nombre_mot']
                    
                    datasource.descripteur_introduction = descripteur_local_conclu
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