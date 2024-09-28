from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .utils import *
@api_view(['POST'])
def send_otp(request):
    phone_no=request.data.get('phone_no')
    if phone_no is None:
        return Response({'message': 'Phone number is required'},status=status.HTTP_400_BAD_REQUEST)
    elif len(phone_no) != 10:
        return Response({'message': 'Invalid phone number'},status=status.HTTP_400_BAD_REQUEST)
    
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




   