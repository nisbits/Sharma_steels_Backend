from django.urls import path

from . import views

urlpatterns = [ 

    path("product-listing/Home-page/", views.product_listing_home_page),
    path("product-listing/catagory/<int:catagory_id>/", views.product_listing_by_catagory),
    path("product-catagory/", views.product_catagory),
    # path("upload-product-excel/", views.upload_product_excel),
    path("product-details/<int:product_id>/", views.product_details)
]
