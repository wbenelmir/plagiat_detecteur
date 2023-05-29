from django import forms

from .models import *

class DatasourceForm(forms.ModelForm):
    
    class Meta:
        model = Datasource
        fields = (
            'code_data',
            'title',
            'doc',
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
                    'accept' : '.pdf',
                    'name': 'doc',
                    'id': 'doc',
                    'maxlength' : '1000',
                },
                
            ),
        }
