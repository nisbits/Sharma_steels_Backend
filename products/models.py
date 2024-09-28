from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=500)
    product_price = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    product_brand = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to="images/")
    stock_quantity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=10)

    def __str__(self):
        return self.product_name