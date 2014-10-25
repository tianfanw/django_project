from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from apps.query.forms import SearchForm

# Create your views here.
def index(request):
  if request.user.is_authenticated():
    # queryForm = QueryForm()
    return redirect('home')
  else:
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, 'index.html', {'login_form': login_form, 'register_form': register_form})

@login_required
def home(request):
  form = SearchForm()
  return render(request, 'home.html', {'form': form})