from rest_framework import viewsets
from .models import LegalContent
from .serializers import LegalContentSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

class LegalContentViewSet(viewsets.ModelViewSet):
    queryset = LegalContent.objects.all()
    serializer_class = LegalContentSerializer

    def get_permissions(self):
        """Allow everyone to view but only admins to edit"""
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
