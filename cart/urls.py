from django.urls import path

from . import views

urlpatterns = [ 

    path("add-to-cart/", views.add_to_cart),
    path('items/', views.cart_items_view),
    path('update-quantity/', views.update_cart_item_quantity),
    path('delete-item/', views.delete_cart_item),
    path('get-subtotal/', views.get_cart_subtotal),
    path('create-order-summary/', views.create_order_summary),
    
]
