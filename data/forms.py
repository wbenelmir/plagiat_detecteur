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

            'pg_titre_nombre_paragraphe',
            'pg_titre_nombre_phrase',
            'pg_titre_nombre_mot',

            'conclusion_nombre_paragraphe',
            'conclusion_nombre_phrase', 
            'conclusion_nombre_mot',

            'introduction_nombre_paragraphe',
            'introduction_nombre_phrase',
            'introduction_nombre_mot',
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
            'pg_titre_nombre_paragraphe': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pg_titre_nombre_paragraphe',
                    'name': 'pg_titre_nombre_paragraphe',
                    'id': 'pg_titre_nombre_paragraphe',
                }
            ),
            'pg_titre_nombre_phrase': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pg_titre_nombre_phrase',
                    'name': 'pg_titre_nombre_phrase',
                    'id': 'pg_titre_nombre_phrase',
                }
            ),
            'pg_titre_nombre_mot': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pg_titre_nombre_mot',
                    'name': 'pg_titre_nombre_mot',
                    'id': 'pg_titre_nombre_mot',
                     'type' : 'number'
                }
            ),
            'conclusion_nombre_paragraphe': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'conclusion_nombre_paragraphe',
                    'name': 'conclusion_nombre_paragraphe',
                    'id': 'conclusion_nombre_paragraphe',
                     'type' : 'number'
                }
            ),
            'conclusion_nombre_phrase': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'conclusion_nombre_phrase',
                    'name': 'conclusion_nombre_phrase',
                    'id': 'conclusion_nombre_phrase',
                     'type' : 'number'
                }
            ),
            'conclusion_nombre_mot': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'conclusion_nombre_mot',
                    'name': 'conclusion_nombre_mot',
                    'id': 'conclusion_nombre_mot',
                     'type' : 'number'
                }
            ),
            'introduction_nombre_paragraphe': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'introduction_nombre_paragraphe',
                    'name': 'introduction_nombre_paragraphe',
                    'id': 'introduction_nombre_paragraphe',
                     'type' : 'number'
                }
            ),
            'introduction_nombre_phrase': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'introduction_nombre_phrase',
                    'name': 'introduction_nombre_phrase',
                    'id': 'introduction_nombre_phrase',
                     'type' : 'number'
                }
            ),
            'introduction_nombre_mot': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'introduction_nombre_mot',
                    'name': 'introduction_nombre_mot',
                    'id': 'introduction_nombre_mot',
                     'type' : 'number'
                }
            ),
        }
