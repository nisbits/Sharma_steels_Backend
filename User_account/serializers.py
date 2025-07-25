from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile , Address # Assuming you have a UserProfile model for phone_number


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)  # Phone number will not be part of User model fields
    user_catagory = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password','phone_number','user_catagory']  # Only User model fields

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')  # Remove phone number from validated data
        user_catagory = validated_data.pop('user_catagory')
        # Create a new User
        user = User.objects.create_user(
            username=phone_number,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Now create the UserProfile entry with phone number
        if user_catagory == "Contractor":
            UserProfile.objects.create(user=user, phone_number=phone_number, user_catagory=user_catagory,admin_approved=False)
        else:
            UserProfile.objects.create(user=user, phone_number=phone_number, user_catagory=user_catagory)
        return user



from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'receiver_name', 'receiver_phone_number', 'address_line_1', 'address_line_2', 'landmark', 'city', 'state', 'zip_code', 'country', 'is_default']



from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  # add more if needed

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user details

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'user_catagory', 'admin_approved', 'contractor_code']
