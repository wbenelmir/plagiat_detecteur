from django.contrib import admin

from .models import *

from import_export.admin import ImportExportModelAdmin



@admin.register(Student)
class StudentsImportExport(ImportExportModelAdmin):
    fields = [
        'code_student',
        'email',
        'first_name',
        'last_name',
        'country',
        'user',
        'password',
    ]
    list_display = [
        'code_student',
        'email',
        'first_name',
        'last_name',
        'country',
        'user',
        'password',
    ]
