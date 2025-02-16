from django.db import models

class LegalContent(models.Model):
    title = models.CharField(max_length=255, unique=True)  # e.g., "Terms and Conditions"
    content = models.TextField()  # HTML content of the policy
    last_updated = models.DateTimeField(auto_now=True)  # Auto update on changes

    def __str__(self):
        return self.title
