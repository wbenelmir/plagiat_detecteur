from django.db import models

from . import data as data_profile
from django.contrib.auth.models import User
import os, random
from django.core.validators import ValidationError

class Datasource(models.Model):
    code_data = models.CharField(
        max_length=200, blank=False, null=False, unique=True)
    
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, blank=True, null=True)          

    def upload_path_doc(self, filename):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        randomstr = ''.join((random.choice(chars)) for x in range(10))

        ext = filename.split('.')[-1]
        filename = "%s.%s" % (randomstr, ext)

        return os.path.join('DataSource/', filename)
    
    def file_size(value): # add this to some file where you can import it from
        limit = 10 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('Fichier trop large. La taille ne doit pas dépasser 2 MB')
    
    doc = models.FileField(upload_to=upload_path_doc, null=True, blank=True, validators=[file_size])

    insert_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        ref = '-'

        if self.code_data:
            ref = str(self.code_data).lower()

        return ref.replace(" ", ".")
