from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
# Create your views here.
from .models import *
from .serializers import *
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
def product_listing_by_catagory(request,catagory_id):
    print(catagory_id)
    products = Product.objects.filter(category=catagory_id)
    if products.count() == 0:
        return Response({"message":"No products found"},status=status.HTTP_404_NOT_FOUND)
    serializer = ProductListingSerializer(products, many=True)
    return Response({"products":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def product_catagory(request):
    catagories = category.objects.all()
    serializer = categorySerializer(catagories, many=True)
    # print(serializer.data)  
    return Response({"catagories":serializer.data},status=status.HTTP_200_OK)

