from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from student.models import *

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password )   

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'L''identifiant ou le mot de passe est incorrect.')
            
    context = {  }
    return render(request, 'login.html', context)

@unauthenticated_user
def register(request):
    
    if request.method == 'POST':

        try:
            password_1 = request.POST.get('password1')
            password_2 = request.POST.get('password2')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
                
            if password_1 == password_2:
                username = str(request.POST.get('email'))
                username = username.replace(' ','')

                User.objects.create(
                            username=username,
                            first_name = first_name,
                            last_name  = last_name ,
                            email  = email ,
                        )
                    
                # Add group to User
                user = User.objects.get(username=username)
                user.set_password(password_1)
                user.save()

                Student.objects.create(
                        code_student     = str(request.POST.get('code_student')),
                        first_name  = first_name,
                        last_name   = last_name,
                        email       = email,
                        user        = user,
                    )
                    

                try:
                    logout(request)    
                except:
                    pass
                    
                return redirect('login')
                
            else:
                messages.error(request,'Les mots de passe ne sont pas identiques')

        except BaseException as e:
            print(str(e))
            print(request,str(e))
            messages.error(request,'Problème lors de l\'inscription.')

            try:
                user.delete()
                ae = Student.objects.get(code_student=request.POST.get('code_student'))
                ae.delete()
            except:
                pass

    context = {  

    }
    return render(request, 'register.html', context)



def logoutuser(request):

    logout(request)    
    return redirect('login')