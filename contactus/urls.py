from django.urls import path
from .views import get_contact_info, post_contact_message

urlpatterns = [
    path("contact-info/", get_contact_info, name="contact-info"),
    path("contact-message/", post_contact_message, name="contact-message"),
]
