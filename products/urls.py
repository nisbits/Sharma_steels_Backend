from django.urls import path

from . import views

urlpatterns = [ 

    path("product-listing/Home-page/", views.product_listing_home_page),
    path("product-listing/catagory/<str:catagory>/", views.product_listing_by_catagory),
    path("product-catagory/", views.product_catagory),
    # path("upload-product-excel/", views.upload_product_excel),
    
]
