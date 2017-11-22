from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from Bot.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

@login_required
def page(request):
	user_obj = UserProfile.objects.get(name=request.user)
	if request.POST:
		form = Form_inscription(request.POST)
		if form.is_valid():
			comment = form.cleaned_data['comment']
			send_mail('New suggestion on railwaybot.pythonanywhere.com', 'Visiter: ' + str(request.user) + '\nEmail: ' + str(user_obj.email) + '\nSuggestion: ' + str(comment), '', ['pyofey.pythonanywhere@gmail.com'])
			return render(request, 'suggestion.html', {'sent': True})
		else:
			return render(request, 'suggestion.html', {'form' : form})
	else:
		form = Form_inscription()
		return render(request, 'suggestion.html', {'form' : form})

class Form_inscription(forms.Form):
	comment = forms.CharField(label="Comment", widget = forms.Textarea(attrs={'class':'materialize-textarea','placeholder':'We value your suggestion'}), max_length=1000)
