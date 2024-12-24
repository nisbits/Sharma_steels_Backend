from django.contrib.auth.models import User
from django.db import models



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    user_catagory = models.CharField(max_length=25)
    admin_approved = models.BooleanField(default=True)
    

from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    receiver_name = models.CharField(max_length=100)  # Name of the person receiving the package
    receiver_phone_number = models.CharField(max_length=15)  # Contact number for delivery
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="India")
    is_default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Check if the user already has any addresses
        if not Address.objects.filter(user=self.user).exists():
            # If no addresses exist, set this address as default
            self.is_default = True
        super().save(*args, **kwargs)  # Call the parent class save method
    def __str__(self):
        return f"{self.receiver_name} - {self.address_line_1}, {self.city}, {self.state}, {self.country}"
