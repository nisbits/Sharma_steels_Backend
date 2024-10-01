from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate
# Create your views here.
from .utils import *
from .models import User, UserProfile

@api_view(['POST'])
def send_otp(request):
    phone_no=request.data.get('phone_no')
    if phone_no is None:
        return Response({'message': 'Phone number is required'},status=status.HTTP_400_BAD_REQUEST)
    elif len(phone_no) != 10:
        return Response({'message': 'Invalid phone number'},status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(phone_number=phone_no).exists():
        return Response({'message': 'User with this Phone number already exists'},status=status.HTTP_409_CONFLICT)
    
    response = send_sms(phone_no)
    print(response.status_code)
    response = response.json()
    if response['Status'] == 'Success':
        return Response({'message': 'OTP sent successfully'},status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def verify_otp(request):
    phone_no = request.data.get('phone_no')
    otp = request.data.get('otp')

    response = verify_sms_phone_no(otp, phone_no)
    print(response.status_code)
    response = response.json()
    
    if response['Status'] == 'Success':
        if response['Details'] == 'OTP Matched':
            return Response({'message': 'OTP verified successfully'},status=status.HTTP_200_OK)
        elif response['Details'] == 'OTP Expired':
            return Response({'message': 'OTP expired'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
    elif response['Status'] == 'Error':
        if response['Details'] == 'OTP Mismatch':
             return Response({'message': 'Invalid OTP'},status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
