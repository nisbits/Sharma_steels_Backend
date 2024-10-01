from django.urls import path

from . import views

urlpatterns = [ 

    path("product-listing/", views.product_listing),
    
]
