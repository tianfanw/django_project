from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
# from apps.account.forms import LoginForm, RegisterForm
from  django.contrib.auth.forms import AuthenticationForm, UserCreationForm

import logging
import time
import requests
import json
from config import CONFIG

# Create your views here.
def login(request):
  if request.user.is_authenticated():
    return redirect('index')
  else:
    if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
        auth_login(request, form.get_user())
        logging.info('login!')
        return redirect('index')
      else:
        logging.info("invalid form")
    else:
      logging.info('not post')
      form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
  if request.user.is_authenticated():
    return redirect('index')
  else:
    if request.method == 'POST':
      form = UserCreationForm(data=request.POST)
      if form.is_valid():
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        auth_login(request, user)
        return redirect('index')
      else:
        logging.info('invalid form')
        
    else:
      form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
  if request.user.is_authenticated():
    # queryForm = QueryForm()
    return render(request, 'index.html')
  else:
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, 'index.html', {'login_form': login_form, 'register_form': register_form})

def getEvents(query):
  base = 'https://api.stubhubsandbox.com'
  resource = '/search/catalog/events/v2'
  params = '?'
  for key, value in query.iteritems():
    if(key == 'date'):
      currentDate = (time.strftime("%Y-%m-%d"))
      params = params + 'date=' + currentDate+'T00:00TO'+value+'T00:00' + '&'
    else:
      params = params + key + '=' + value + '&'

  headers = {
    'Accept-Encoding'  : 'application/json',
    'Authorization' : 'Bearer ' + CONFIG['stubhub']['application_token']
  }
  
  req = requests.get(base+resource+params, headers=headers, verify=False)
  if req.status_code == 200:
    res = req.json()
    if res['numFound'] == 0:
      return {'error': 'No records found.'}
    else:
      return res
  else:
    return {'error': req.status_code}
  
  # return {'error': 'test'}

@login_required
def search(request):
  query = request.GET
  if not query:
    return render(request, 'search.html')
  else:
    logging.info(query)
    result = getEvents(query)
    return render(request, 'search.html', {'result': result})