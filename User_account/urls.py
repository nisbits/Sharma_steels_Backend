from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("send-otp/", send_otp),
    path("verify-otp/", verify_otp),
    path('register/', register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login_view, name='login'),
    path('addresses/', manage_addresses, name='manage_addresses'),  # List and add addresses
    path('addresses/delete/<int:address_id>/', delete_address, name='delete_address'),  # Delete address
    path('addresses/set-default/<int:address_id>/', set_default_address, name='set_default_address'),  # Set default address
    path('mydetails/', get_current_user_details, name='current-user-details'),
]



