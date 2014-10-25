from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from apps.query.forms import SearchForm
# Create your views here.

@login_required
def search(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      # process data somehow
      results = {}
      results['results_field1'] = cd['search_field1'] + cd['search_field2'] + cd['search_field3']
      results['results_field2'] = cd['search_field3'] + cd['search_field2'] + cd['search_field1']
      return render(request, 'search.html', {'form': form, 'results': results})
  else:
    form = SearchForm()
  return render(request, 'search.html', {'form': form})

# @login_required
# def results(request):
#   logger.info(request)
#   return render(request, 'results.html')