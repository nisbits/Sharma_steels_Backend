from rest_framework import serializers
from .models import LegalContent

class LegalContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalContent
        fields = ["id", "title", "content", "last_updated"]
