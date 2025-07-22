from django.contrib.auth.models import User
from django.db import models



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    user_catagory = models.CharField(max_length=25)
    admin_approved = models.BooleanField(default=True)
    contractor_code = models.CharField(max_length=10, blank=True, null=True, unique=True)
    
    def save(self, *args, **kwargs):
        # Generate contractor code only for contractor users and only if not already set
        if self.user_catagory == 'Contractor' and not self.contractor_code:
            # Get the last contractor code and increment
            last_profile = UserProfile.objects.filter(
                user_catagory='Contractor'
            ).exclude(contractor_code__isnull=True).order_by('-contractor_code').first()

            if last_profile and last_profile.contractor_code:
                # Extract the numeric part and increment
                last_number = int(last_profile.contractor_code.replace('CTR', ''))
                new_number = last_number + 1
            else:
                new_number = 1  # start from 1

            self.contractor_code = f"CTR{new_number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    

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
