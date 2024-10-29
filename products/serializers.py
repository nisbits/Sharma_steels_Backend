from rest_framework import serializers
from .models import *

class ProductListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id','discount','product_image_main','brand_name','specification','mrp','selling_price','unit_of_measurement']

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"


class productImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class productDetailsSerializer(serializers.ModelSerializer):
    additional_images = productImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['product_id','category','brand_name','specification','mrp','in_stock','discount','product_image_main','unit_of_measurement','selling_price','minimum_order_quantity','description','additional_images']


