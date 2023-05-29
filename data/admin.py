from django.contrib import admin

from .models import *

from import_export.admin import ImportExportModelAdmin

@admin.register(Datasource)
class DatasourceImportExport(ImportExportModelAdmin):
    fields = [
            'code_data',
            'title',
            'doc',
    ]
    list_display = [
            'code_data',
            'title',
            'doc',
    ]
