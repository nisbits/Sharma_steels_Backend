from django.db import models

class ContactInfo(models.Model):
    """Stores static business contact details."""
    owner_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updates when edited

    def __str__(self):
        return f"Contact Info of {self.owner_name}"

class ContactMessage(models.Model):
    """Stores messages sent by users from the contact form."""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Saves timestamp

    def __str__(self):
        return f"Message from {self.name}"
