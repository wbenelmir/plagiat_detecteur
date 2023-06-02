from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from authentification.decorators import *

from data.analyse import *
from django.conf import settings

from django.conf import settings
from data.models import *

import os
import shutil

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
def analyse(request, code_data):

    datasource = Datasource.objects.get(code_data=code_data)

    titres = []

    discripteur= Segmentation('media/archive')

    titres = concatener_mots_titres(discripteur)
    titres_pertinents=rechercher_titres_similaires(datasource.titres_pages_de_garde, titres)
    descripteur_pertinent=recuperer_descripteur(titres_pertinents, discripteur)

    # print(descripteur_pertinent)
    codes_pages_de_garde = descripteur_pertinent['codes_pages_de_garde']
    titres_pages_de_garde = descripteur_pertinent['titres_pages_de_garde']
    liens_descripteurs_locaux = descripteur_pertinent['liens_descripteurs_locaux']

    _titre = []
    _conclusion = []
    _introductuion = []

    titres_pg = []
    codes_pg = []

    for el in titres_pages_de_garde:
        titres_pg.append(el)

    for el in codes_pages_de_garde:
        codes_pg.append(el)

    for el in liens_descripteurs_locaux:
        # print(el)
        if el['type'] == 'titre':
            _titre.append(el)
        elif el['type'] == 'conclusion':
            _conclusion.append(el)
        elif el['type'] == 'introductuion':
            _introductuion.append(el)


    titre = []
    conclusion = []
    introductuion = []

    nombre_paragraphe = []
    nombre_phrase = []
    nombre_mot = []
    

    for el in _titre:
        nombre_paragraphe.append(el['lien']['nombre_paragraphe'])
        nombre_phrase.append(el['lien']['nombre_phrase'])
        nombre_mot.append(el['lien']['nombre_mot'])
    titre.append(nombre_paragraphe)
    titre.append(nombre_phrase)
    titre.append(nombre_mot)

    nombre_paragraphe = []
    nombre_phrase = []
    nombre_mot = []

    for el in _conclusion:
        nombre_paragraphe.append(el['lien']['nombre_paragraphe'])
        nombre_phrase.append(el['lien']['nombre_phrase'])
        nombre_mot.append(el['lien']['nombre_mot'])
    conclusion.append(nombre_paragraphe)
    conclusion.append(nombre_phrase)
    conclusion.append(nombre_mot)

    nombre_paragraphe = []
    nombre_phrase = []
    nombre_mot = []

    for el in _introductuion:
        nombre_paragraphe.append(el['lien']['nombre_paragraphe'])
        nombre_phrase.append(el['lien']['nombre_phrase'])
        nombre_mot.append(el['lien']['nombre_mot'])
    introductuion.append(nombre_paragraphe)
    introductuion.append(nombre_phrase)
    introductuion.append(nombre_mot)

    print(introductuion)
    context = {
        'datasource' : datasource,

        'titres_pg' : titres_pg,
        'codes_pg' : codes_pg,

        'titre' : titre,
        'conclusion' : conclusion,
        'introductuion' : introductuion,

    }

    return render(request, 'analyse/show.html', context)
