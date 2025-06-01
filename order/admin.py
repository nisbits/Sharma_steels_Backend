from django.contrib import admin

# Register your models here.
from .models import Order, OrderAddresses
from django.urls import reverse
from django.utils.html import format_html
class OrderAddressesInline(admin.TabularInline):  # or use admin.TabularInline for a table format
    model = OrderAddresses
    extra = 0  # Do not show extra empty forms


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','get_order_summary_id','status','total_price','payment_status','razorpay_tracking_id','created_at','updated_at','get_address','view_order_items')  # Fields shown in table
    list_filter = ('status','payment_status')  # Sidebar filters
    search_fields = ('id',)  # Search bar for orders
    ordering = ('-id',)  # Orders sorted by newest first
    list_per_page = 20  # Number of records per page
    inlines = [OrderAddressesInline]
    def get_order_summary_id(self, obj):
        return str(obj.order_summary.id )if hasattr(obj, 'order_summary') else "N/A"

    def get_address(self, obj):
        """
        Returns the complete address of the order if it has an associated OrderAddresses.
        """
        if hasattr(obj, 'order_address'):  # Check if OrderAddresses exists
            address = obj.order_address  # Get the related OrderAddresses instance
            return f"{address.address_line_1}, {address.address_line_2 or ''}, {address.landmark or ''}, {address.city}, {address.state}, {address.zip_code}, {address.country}"
        return "No Address Available"  # If no address exists
    
    get_address.short_description = "Address"

    def view_order_items(self, obj):
        url = reverse('admin:cart_ordersummaryitem_changelist') + f'?order_summary__id__exact={obj.order_summary.id}'
        return format_html('<a href="{}" style="color: blue; font-weight: bold;">View Items</a>', url)
    view_order_items.short_description = "Order Items"  # Column header in the admin panel


admin.site.register(Order, OrderAdmin)  # Register the model with admin


class OrderAddressesAdmin(admin.ModelAdmin):
    list_display = ('order','receiver_name','receiver_phone_number','address_line_1','address_line_2','landmark','city','state','zip_code','country')  # Fields shown in table
    # list_filter = ('',)  # Sidebar filters
    search_fields = ('receiver_name',)  # Search bar for orders
    ordering = ('order',)  # Orders sorted by newest first
    list_per_page = 20  # Number of records per page

admin.site.register(OrderAddresses, OrderAddressesAdmin)  # Register the model with admin