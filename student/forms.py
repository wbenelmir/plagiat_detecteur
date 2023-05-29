from django import forms

from .models import *

class BasicInfoForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'code_student',
            'first_name',
            'last_name',
            'country',
            'email',
            'domain',
        )

        widgets = {
            'code_student': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Code',
                    'name': 'code_student',
                    'id': 'code_student',
                    'style' : 'text-transform: uppercase'
                }
            ),
            'last_name': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'name': 'last_name',
                    'id': 'last_name',
                    'placeholder': 'Nom',
                }
            ),
            'first_name': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'name': 'first_name',
                    'id': 'first_name',
                    'placeholder': 'Prénom',
                }
            ),
            'country': forms.Select
            (
                attrs={
                    'class': 'form-select',
                    'name': 'country',
                    'id': 'country',
                    'placeholder': 'Location',
                }
            ),
            'email': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Adresse Email',
                    'name': 'email',
                    'id': 'email',
                    'type': 'email'
                }
            ),
            'domain': forms.Select
            (
                attrs={
                    'class': 'form-select',
                    'name': 'domain',
                    'id': 'domain',
                    'placeholder': 'Domain',
                }
            ),
        }

class ContactInfo(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'phone',
            'linkedin',
            'email',
        )

        widgets = {
            #<input type="text" class="form-control mob_no fill" data-mask="9999-999-999">
            'phone': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'name': 'phone',
                    'id': 'phone',
                    'placeholder': '(+213) 555 213 245',
                }
            ),
            'linkedin': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'name': 'linkedin',
                    'id': 'linkedin',
                    'placeholder': 'Lien vers le profil LinkedIn',
                }
            ),
            'email': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Adresse Email',
                    'name': 'email',
                    'id': 'email',
                    'type': 'email'
                }
            ),
        }

class UserContactForm(forms.ModelForm):
    
    class Meta:
        model = UserContact
        fields = (
            'code_contact',
            'user',
            'student',
            'subject',
            'msg',
        )

        widgets = {
            'code_contact': forms.TextInput
            (
                attrs={
                    'class': 'form-control form-control-capitalize',
                    'placeholder': 'Invitation Code',
                    'name': 'code_contact',
                    'id': 'code_contact',
                    'style' : 'text-transform: uppercase'
                }
            ),
            'user': forms.Select
            (
                attrs={
                    'class': 'form-select',
                    'name': 'user',
                    'id': 'user',
                }
            ),
            'student': forms.Select
            (
                attrs={
                    'class': 'form-select',
                    'name': 'student',
                    'id': 'student',
                    'placeholder': 'Utilisateur',
                }
            ),
            'subject': forms.TextInput
            (
                attrs={
                    'class': 'form-control',
                    'name': 'subject',
                    'id': 'subject',
                    'style': 'margin-bottom:10px;',
                    'placeholder': 'Titre',
                }
            ),
            'msg': forms.Textarea
            (
                attrs={
                    'name': 'msg',
                    'id': 'msg',
                    'placeholder': 'Message..',
                    'style': 'margin-top:10px;',
                }
            ),
        }
