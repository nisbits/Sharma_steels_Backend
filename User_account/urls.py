from django.urls import path
from .views import *
urlpatterns = [
    path("send-otp/", send_otp),
    path("verify-otp/", verify_otp),
]