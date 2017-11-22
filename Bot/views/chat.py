from django.shortcuts import render

def page(request):
	return render(request, 'chat.html',{})