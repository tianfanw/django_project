from django.contrib.auth.forms import UserCreationForm
from django import forms

class LoginForm(UserCreationForm):
	email = forms.EmailField()
	
	def save(self, *args, **kwargs):
		user = super(RegisterForm, self).save(*args, **kwargs)
		user.email = self.cleaned_data["email"]
		user.save()
		
		return user