from django.db import models
from django.contrib.auth.models import User
from products.models import *
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product.specification} - {self.quantity}"
    def save(self, *args, **kwargs):
        # Calculate total price based on quantity and price
        if self.price is None:
              pass
        else:
            self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

# q: What is the purpose of the OrderSummary model?
# a: The OrderSummary model is used to store the summary of an order, including the total price and the user who placed the order. It acts as a record of the order details for reference and tracking purposes.
from User_account.models import Address

class OrderSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False) # logic is pending in views
    def calculate_total_price(self):
        # Calculate the sum of total prices for each item in the order summary
        total = sum(item.total_price for item in self.items.all())
        
        # Set the total price of the order summary
        self.total_price = total
        
        # Save the updated total price to the database
        self.save()
class OrderSummaryItem(models.Model):
    order_summary = models.ForeignKey(OrderSummary, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price per item
    extra_charges = models.ManyToManyField(ExtraCharge, blank=True, related_name="order_items")  # Multiple extra charges
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total price including charges
    
    def __str__(self):
        return f"{self.product.specification} - {self.quantity} pcs"
    def calculate_total_price(self):
        # Base price calculation
        self.total_price = self.price * self.quantity

        # Add each extra charge amount to the total
        for charge in self.extra_charges.all():
            if charge.amount_known:  
                self.total_price += charge.amount * self.quantity

        self.save()

# create a func to add two models to the cart   