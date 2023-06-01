from django.contrib import admin

from .models import *

from import_export.admin import ImportExportModelAdmin

@admin.register(Datasource)
class DatasourceImportExport(ImportExportModelAdmin):
    fields = [
            'code_data',
            'title',
            'doc',

            'codes_pages_de_garde',
            'titres_pages_de_garde',

            'pg_titre_nombre_paragraphe',
            'pg_titre_nombre_phrase',
            'pg_titre_nombre_mot',

            'conclusion_nombre_paragraphe',
            'conclusion_nombre_phrase', 
            'conclusion_nombre_mot',

            'introduction_nombre_paragraphe',
            'introduction_nombre_phrase',
            'introduction_nombre_mot',

            'descripteur_global',
            'descripteur_conclusion',
            'descripteur_introduction',
            
    ]
    list_display = [
            'code_data',
            'title',
            'doc',

            'codes_pages_de_garde',
            'titres_pages_de_garde',

            'pg_titre_nombre_paragraphe',
            'pg_titre_nombre_phrase',
            'pg_titre_nombre_mot',

            'conclusion_nombre_paragraphe',
            'conclusion_nombre_phrase', 
            'conclusion_nombre_mot',

            'introduction_nombre_paragraphe',
            'introduction_nombre_phrase',
            'introduction_nombre_mot',

            'descripteur_global',
            'descripteur_conclusion',
            'descripteur_introduction',
    ]

