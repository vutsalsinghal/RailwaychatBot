from django.shortcuts import render
from Bot.models import UserProfile

def page(request):
	return render(request, 'index.html',{})