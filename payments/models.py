from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from order.models import  Order
class Payment(models.Model):
    PAYMENT_MODES = [
        ('online', 'Online'),
        ('cod', 'Cash on Delivery'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Link to the order
    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODES,
        default='online',
    )
    razorpay_order_id = models.CharField(max_length=255, unique=True,null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(
        max_length=20,
        choices=[('created', 'Created'), ('successful', 'Successful'), ('failed', 'Failed')],
        default='created'
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.razorpay_payment_id} - {self.status}"