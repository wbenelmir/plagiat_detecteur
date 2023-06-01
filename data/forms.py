from django import forms

from .models import *

class DatasourceForm(forms.ModelForm):
    
    class Meta:
        model = Datasource
        fields = (
            'code_data',
            'title',
            'doc',
            'codes_pages_de_garde',
            'titres_pages_de_garde',
            'liens_descripteurs_locaux_type',
            'nombre_paragraphe',
            'nombre_phrase',
            'nombre_mot',
        )

        widgets = {
            'code_data': forms.TextInput
            (
                attrs={
                    'class': 'form-control form-control-capitalize',
                    'placeholder': 'Invitation Code',
                    'name': 'code_data',
                    'id': 'code_data',
                    'style' : 'text-transform: uppercase'
                }
            ),
            'title': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'name': 'title',
                    'id': 'title',
                    'style': 'margin-bottom:10px;',
                    'placeholder': 'Titre',
                }
            ),
            'doc': forms.FileInput
            (
                attrs={
                    'class': 'font-weight-bold custom-file-input',
                    'accept' : '.docx',
                    'name': 'doc',
                    'id': 'doc',
                    'maxlength' : '1000',
                },
                
            ),
            'codes_pages_de_garde': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'codes_pages_de_garde',
                    'name': 'codes_pages_de_garde',
                    'id': 'codes_pages_de_garde',
                }
            ),
            'titres_pages_de_garde': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'titres_pages_de_garde',
                    'name': 'titres_pages_de_garde',
                    'id': 'titres_pages_de_garde',
                }
            ),
            'liens_descripteurs_locaux_type': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'liens_descripteurs_locaux_type',
                    'name': 'liens_descripteurs_locaux_type',
                    'id': 'liens_descripteurs_locaux_type',
                }
            ),
            'liens_descripteurs_locaux_type': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'liens_descripteurs_locaux_type',
                    'name': 'liens_descripteurs_locaux_type',
                    'id': 'liens_descripteurs_locaux_type',
                }
            ),
            'nombre_paragraphe': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'nombre_paragraphe',
                    'name': 'nombre_paragraphe',
                    'id': 'nombre_paragraphe',
                     'type' : 'number'
                }
            ),
            'nombre_phrase': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'nombre_phrase',
                    'name': 'nombre_phrase',
                    'id': 'nombre_phrase',
                     'type' : 'number'
                }
            ),
            'nombre_mot': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'nombre_mot',
                    'name': 'nombre_mot',
                    'id': 'nombre_mot',
                     'type' : 'number'
                }
            ),
        }
