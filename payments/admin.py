# from django.contrib import admin
# from.models import Payment
# admin.site.register(Payment)
# Register your models here.
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'order',
        'payment_mode',
        'razorpay_order_id',
        'razorpay_payment_id',
        'amount',
        'currency',
        'status',
        'created_at',
        'updated_at',
    ]

    list_filter = ['status', 'payment_mode', 'currency', 'created_at']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id', 'user__username', 'order__id']
    ordering = ['-created_at']