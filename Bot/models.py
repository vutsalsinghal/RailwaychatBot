from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
	user_auth      = models.OneToOneField(User, primary_key=True, help_text="Uername should be unique")
	name           = models.CharField(max_length=50, verbose_name="Name")
	email          = models.EmailField(verbose_name="Email")
	password       = models.CharField(max_length=100, verbose_name="Password")
	activation_key = models.CharField(max_length=64, blank=True)
	key_expires    = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user_auth.username