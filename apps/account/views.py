from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.http import HttpResponse
# from apps.account.forms import LoginForm, RegisterForm
from  django.contrib.auth.forms import AuthenticationForm, UserCreationForm

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def login(request):
  if request.user.is_authenticated():
    return redirect('home')
  else:
    if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
        auth_login(request, form.get_user())
        logger.info('login!')
        return redirect('index')
      else:
        logger.info("invalid form")
    else:
      logger.info('not post')
      form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
  if request.user.is_authenticated():
    return redirect('home')
  else:
    if request.method == 'POST':
      form = UserCreationForm(data=request.POST)
      if form.is_valid():
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        auth_login(request, user)
        return redirect('index')
      else:
        logger.info('invalid form')
        
    else:
      form = UserCreationForm()
    return render(request, 'register.html', {'form': form})