from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage
# Register your models here.
admin.site.site_header = "Sharma_steels"
admin.site.register(Product)
admin.site.register(ProductImage)
