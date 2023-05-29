from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.db import connection

@login_required(login_url='login')
def index(request):

    context = {

    }
    return render(request, 'index.html', context)
