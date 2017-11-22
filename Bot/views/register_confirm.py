from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from Bot.models import UserProfile

def page(request, activation_key):
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if user_profile.key_expires < timezone.now():
        return render_to_response('confirm_expired.html')
    else:
        user_profile.user_auth.is_active = True
        user_profile.user_auth.save()
        return render(request, 'register_success.html',{})
