# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from cart.models import OrderSummary
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_summary = models.OneToOneField(OrderSummary, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Final price of the order
    payment_status = models.BooleanField(default=False)  # Payment made or not
    razorpay_tracking_id = models.CharField(max_length=100, null=True, blank=True)  # Razorpay Order ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderAddresses(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_address')
    receiver_name = models.CharField(max_length=100)  # Name of the person receiving the package
    receiver_phone_number = models.CharField(max_length=15)  # Contact number for delivery
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default="India")

    def __str__(self):
        return f"{self.receiver_name} - {self.address_line_1}, {self.city}, {self.state}, {self.country}"
