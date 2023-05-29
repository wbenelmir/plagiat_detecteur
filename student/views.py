from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db import connection

from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from authentification.decorators import *

@login_required(login_url='login')
def basicInfo(request):
    print('basicInfo')
    try:
        student = Student.objects.get(user__username = request.user)
    except:
        return redirect('home')
    
    basicInfoForm = BasicInfoForm(instance=student)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        basicInfoForm = BasicInfoForm(request.POST, request.FILES, instance=student)
        # check whether it's valid:
        if basicInfoForm.is_valid():
            basicInfoForm.save()

            messages.success(request, 'Les informations ont été envoyées avec succès.')
            redirect('../../../std/basicInfo')
        else:
            messages.error(request,'Une erreur s\'est produite.')
            print(basicInfoForm.errors)

        # print(basicInfo_studentForm.errors)

    try:
        student = Student.objects.get(user__username = request.user)
        if student.country:
            country = student.country
        else:
            country = 'Algeria'

    except:
        pass

    context = {
        'basicInfoForm' : basicInfoForm,
        'country' : country,
        'student' : student,
    }
    return render(request, 'student/basicInfo.html', context)

@login_required(login_url='login')
def contactInfo(request):
    
    try:
        student = Student.objects.get(user__username = request.user)
    except:
        return redirect('home')
    
    contactInfo = ContactInfo(instance=student)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        contactInfo = ContactInfo(request.POST, instance=student)
        # check whether it's valid:
        if contactInfo.is_valid():
            contactInfo.save()

            messages.success(request, 'Les informations ont été envoyées avec succès.')
            redirect('../../../std/basicInfo')
        else:
            messages.error(request,'Une erreur s\'est produite.')
            print(contactInfo.errors)

        # print(ContactInfo.errors)

    context = {
        'contactInfo' : contactInfo,
        'student' : student,
    }
    return render(request, 'student/contactInfo.html', context)



@login_required(login_url='login')
def user_contact(request):

    try:
        student = Student.objects.get(user__username = request.user)
    except:
        student = None

    try:
        user = User.objects.get(username = request.user)
    except:
        user = None
    
    contactForm = UserContactForm()
    if request.method == 'POST':
        contactForm = UserContactForm(request.POST)
        # check whether it's valid:
        if contactForm.is_valid():
            contactForm.save()
            try:
                userContact = UserContact.objects.get(code_contact=request.POST.get('code_contact'))
                if student:
                    userContact.student = student
                    userContact.save()
                if user:
                    userContact.user = user
                    userContact.save()

            except BaseException as e:
                print(str(e))
            messages.success(request, 'Le message a été envoyé avec succès.')
        else:
            messages.error(request,'Une erreur s\'est produite lors de l\'envoi du message.')
            print(contactForm.errors)

    context = {
        'contactForm' : contactForm,
        'student' : student
    }
    return render(request, 'student/contact.html', context)
