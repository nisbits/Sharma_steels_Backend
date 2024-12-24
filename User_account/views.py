from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate 
# Create your views here.
from .utils import *
from .models import User, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
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
    print("response from 2factor: ",response.status_code)
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

from rest_framework_simplejwt.tokens import RefreshToken
@api_view(['POST'])
def login_view(request):
    phone_no = request.data.get('phone_no')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(username=phone_no, password=password)

    if user is not None:
        try:
            # Get the profile associated with the user
            profile = UserProfile.objects.get(user=user)

            # Check if the admin has approved the account
            if not profile.admin_approved:
                return Response({'detail': 'Your account is not yet approved by the admin.'}, status=status.HTTP_403_FORBIDDEN)

            # Generate JWT tokens if user is admin-approved
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            refresh['first_name'] = user.first_name
            refresh['last_name'] = user.last_name
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        except UserProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@api_view(['GET', 'POST'])
def manage_addresses(request):
    if request.method == 'GET':
        # List all addresses for the logged-in user
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response({"user_Addresses":serializer.data})
    
    elif request.method == 'POST':
        # Create a new address
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"user_Addresses":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_address(request, address_id):
    # Delete an address by ID
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def set_default_address(request, address_id):
    # Set a specific address as the default
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    # Unset previous default address, if any
    Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
    
    # Set the new default address
    address.is_default = True
    address.save()
    
    return Response({"message": "Default address set successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_default_address(request):
    # Get the default address for the logged-in user
    address = get_object_or_404(Address, user=request.user, is_default=True)
    serializer = AddressSerializer(address)
    return Response(serializer.data)