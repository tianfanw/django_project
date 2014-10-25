from django import forms

class SearchForm(forms.Form):
    search_field1 = forms.CharField(label='Search Field 1', max_length=100)
    search_field2 = forms.CharField(label='Search Field 2', max_length=100)
    search_field3 = forms.CharField(label='Search Field 3', max_length=100)
