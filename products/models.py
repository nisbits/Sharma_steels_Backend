from django.db import models

class category(models.Model):
    catagory=models.CharField(max_length=255)
    catagory_image=models.ImageField(upload_to='catagory_images/')
    def __str__(self):
        return self.catagory

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category =  models.ForeignKey(category, on_delete=models.CASCADE)     # Category of the product
    brand_name = models.CharField(max_length=255)
    specification = models.TextField()
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    product_image_main = models.ImageField(upload_to='product_images/', null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    minimum_order_quantity = models.PositiveIntegerField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # If discount is provided, calculate selling price
        if self.discount:
            self.selling_price = self.mrp - (self.mrp * self.discount / 100)
        else:
            self.selling_price = self.mrp  # No discount, selling price is same as MRP

        # Call the original save() method to save the object
        super().save(*args, **kwargs)

    def __str__(self):
        return self.specification
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/additional/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Additional Image for {self.product.product_name}"
    
class ExtraCharge(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="extra_charges")
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name