from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError


'''For Login of the user '''

class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)

    def check_user(self, cleaned_data):
        email_or_phone = cleaned_data.get('email_or_phone')
        password = cleaned_data.get('password')

        # Check if the input is an email address
        if '@' in email_or_phone:
            # Authenticate using email
            user = authenticate(email=email_or_phone, password=password)
        else:
            # Authenticate using phone number
            user = authenticate(phone_number=email_or_phone, password=password)

        if not user:
            raise ValidationError('User not found or invalid credentials')

        return user