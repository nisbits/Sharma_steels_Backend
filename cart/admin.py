from django.contrib import admin
from .models import Cart, CartItem, OrderSummary, OrderSummaryItem
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
admin.site.register( 
    [Cart, CartItem,]
    
)

class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('id','user','created_at', 'total_price','address','is_confirmed','view_order_items')  # Fields shown in table
    list_filter = ('is_confirmed',)  # Sidebar filters
    search_fields = ('id',)  # Search bar for orders
    ordering = ('user',)  # Orders sorted by newest first
    list_per_page = 20  # Number of records per page

    def view_order_items(self, obj):
        url = reverse('admin:cart_ordersummaryitem_changelist') + f'?order_summary__id__exact={obj.id}'
        return format_html('<a href="{}" style="color: blue; font-weight: bold;">View Items</a>', url)


    view_order_items.short_description = "View Items"

admin.site.register(OrderSummary, OrderSummaryAdmin) 


class OrderSummaryItemAdmin(admin.ModelAdmin):
    list_display = ('order_summary','product', 'quantity','price','get_extra_charges','total_price')  # Fields shown in table
    list_filter = ('quantity',)  # Sidebar filters
    search_fields = ('quantity',)  # Search bar for orders
    ordering = ('quantity',)  # Orders sorted by newest first
    list_per_page = 20  # Number of records per page

    def get_extra_charges(self, obj):
        return ", ".join([charge.name for charge in obj.extra_charges.all()])

admin.site.register(OrderSummaryItem, OrderSummaryItemAdmin)  # Register the model with admin