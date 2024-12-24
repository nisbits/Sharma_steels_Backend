from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now

# class Payment(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to the user
#     order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Link to the order
#     razorpay_order_id = models.CharField(max_length=255, unique=True)
#     razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
#     razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=10, default='INR')
#     status = models.CharField(
#         max_length=20,
#         choices=[('created', 'Created'), ('successful', 'Successful'), ('failed', 'Failed')],
#         default='created'
#     )
#     created_at = models.DateTimeField(default=now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Payment {self.razorpay_payment_id} - {self.status}"