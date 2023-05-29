from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

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


def logoutuser(request):

    logout(request)    
    return redirect('login')