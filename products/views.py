from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
# Create your views here.
from .models import Product, ProductImage
from .serializers import ProductListingSerializer
from rest_framework import status
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_listing_home_page(request):
    products = Product.objects.all().order_by('?')
    serializer = ProductListingSerializer(products, many=True)
    return Response({"products":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_listing_by_catagory(request,catagory):
    print(catagory)
    products = Product.objects.filter(category__iexact=catagory)
    if products.count() == 0:
        return Response({"message":"No products found"},status=status.HTTP_404_NOT_FOUND)
    serializer = ProductListingSerializer(products, many=True)
    return Response({"products":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_catagory(request):
    unique_catagories = ['Cement','Tmt','Ring(Churi)','Bending Wire']
    additionals=['Stone Chips','Bricks','Paints','Cover Blocks','Chemicals']
    unique_catagories.extend(additionals)
    return Response({"catagories":unique_catagories},status=status.HTTP_200_OK)

