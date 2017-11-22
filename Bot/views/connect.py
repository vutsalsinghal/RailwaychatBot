from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from Bot.models import UserProfile

def page(request):
	if request.POST:
		form = Form_connection(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)				
				if request.GET.get('next') is not None:
					return redirect(request.GET['next'])
				else:
					return redirect('index')

		else:
			return render(request, 'index.html', {'form' : form})
	else:
		form = Form_connection()
	return render(request, 'connect.html', {'form' : form})

class Form_connection(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	def clean(self):
		cleaned_data = super(Form_connection, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if not authenticate(username=username, password=password):
			raise forms.ValidationError("Wrong login or passwsord")
		return self.cleaned_data