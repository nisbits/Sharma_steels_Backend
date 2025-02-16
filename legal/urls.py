from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LegalContentViewSet

router = DefaultRouter()
router.register(r"", LegalContentViewSet, basename="legal-content")

urlpatterns = [
    path("", include(router.urls)),
]
