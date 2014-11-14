from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
# from apps.account.forms import LoginForm, RegisterForm
from  django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import Http404 
import logging
import stubhub

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

@login_required
def search(request):
  query = request.GET
  if not query:
    return render(request, 'search.html')
  else:
    logging.info(query)
    result = stubhub.getEvents(query)
    logging.info(result)
    return render(request, 'search.html', {'result': result})

def tickets(request):
  eventId = request.GET.get('eventId')
  if not eventId:
    return render(request, 'tickets.html', {'error': '404 not found'})
  else:
    result = stubhub.getTickets(eventId)
    return render(request, 'tickets.html', {'result': result})