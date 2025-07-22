from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
     path('my-orders/', views.get_user_orders, name='my-orders'),
]

