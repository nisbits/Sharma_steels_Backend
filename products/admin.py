from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.site_header = "Sharma_steels"
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(category)
admin.site.register(ExtraCharge)

