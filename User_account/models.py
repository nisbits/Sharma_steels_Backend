from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    user_catagory = models.CharField(max_length=25)
    admin_approved = models.BooleanField(default=True)
    

