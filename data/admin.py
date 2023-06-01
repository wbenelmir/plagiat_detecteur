from django.contrib import admin

from .models import *

from import_export.admin import ImportExportModelAdmin

@admin.register(Datasource)
class DatasourceImportExport(ImportExportModelAdmin):
    fields = [
            'code_data',
            'title',
            'codes_pages_de_garde',
            'titres_pages_de_garde',
            'liens_descripteurs_locaux_type',
            'nombre_paragraphe',
            'nombre_phrase',
            'nombre_mot',
            'is_archive',
            
    ]
    list_display = [
            'code_data',
            'title',
            'codes_pages_de_garde',
            'titres_pages_de_garde',
            'liens_descripteurs_locaux_type',
            'nombre_paragraphe',
            'nombre_phrase',
            'nombre_mot',
            'is_archive',
    ]

