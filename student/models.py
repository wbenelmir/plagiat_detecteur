from django.db import models

from . import data as data_student

from django.contrib.auth.models import User
import os, random
from django.core.validators import ValidationError

class Student(models.Model):
    code_student = models.CharField(max_length=200, blank=False, null=False, unique=True)
    
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    password = models.CharField(max_length=200, blank=True, null=True)          # intial password
    email = models.CharField(
        max_length=200, blank=False, null=False)
    first_name = models.CharField(max_length=200, blank=True, null=True, default="-")
    last_name = models.CharField(max_length=200, blank=True, null=True, default="-")

    domain = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        choices=data_student.domain.choices,
        default=data_student.domain.nule
    )

    country = models.CharField(max_length=200, blank=True, null=True)

    phone = models.CharField(max_length=500, blank=True, null=True)
    linkedin = models.CharField(max_length=500, blank=True, null=True)

    insert_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        ref = '-'

        if self.first_name:
            ref = str(self.first_name).lower()

        if self.first_name:
                ref = str(self.last_name).lower()

        return ref.replace(" ", ".")

class UserContact(models.Model):
    code_contact = models.CharField(
        max_length=200, blank=False, null=False, unique=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)

    subject = models.CharField(max_length=200, blank=True, null=True)
    msg = models.CharField(max_length=2040, blank=False, null=False)

    insert_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        ref = '-'
    
        if self.code_contact:
            ref = str(self.code_contact)

        return ref.replace(" ", ".")