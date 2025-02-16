from rest_framework import serializers
from .models import ContactInfo, ContactMessage

class ContactInfoSerializer(serializers.ModelSerializer):
    """Serializer for business contact details."""
    class Meta:
        model = ContactInfo
        fields = "__all__"

class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for messages sent by users."""
    class Meta:
        model = ContactMessage
        fields = "__all__"
