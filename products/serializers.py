from rest_framework import serializers
from .models import Product

class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['discount','product_image_main','brand_name','specification','mrp','selling_price','unit_of_measurement']