from django.db import models
from products.models import Product
from order.models import Order
# Create your models here.
class PointSystem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    minimum_quantity = models.PositiveIntegerField()
    points_awarded = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.specification} - {self.minimum_quantity}+ qty = {self.points_awarded} points"
    

class ContractorPoints(models.Model):
    contractor_code = models.CharField(max_length=100)  # entered by admin
    order_id = models.CharField(max_length=100, unique=True)  # entered by admin
    points = models.IntegerField(blank=True, null=True)  # auto-calculated

    def save(self, *args, **kwargs):
        if self.order_id:
            total_points = 0
            order_obj= Order.objects.get(id=self.order_id)
            summart_obj = order_obj.order_summary
            items = summart_obj.items.all()

            for item in items:
                try:
                    rule = PointSystem.objects.get(product=item.product)
                    if item.quantity >= rule.minimum_quantity:
                        multiplier = item.quantity // rule.minimum_quantity
                        total_points += multiplier * rule.points_awarded
                except PointSystem.DoesNotExist:
                    continue

            self.points = total_points

        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.contractor_code}, Order ID: {self.order_id}, Points: {self.points}"
    


    # models.py
class ContractorPointSummary(models.Model):
    contractor_code = models.CharField(max_length=50, unique=True)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.contractor_code} - {self.total_points} points"
