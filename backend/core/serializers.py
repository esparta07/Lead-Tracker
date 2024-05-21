from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from django.contrib.auth import (
    get_user_model,
    authenticate,
)



from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['phone_number', 'password', 'full_name', 'email', 'user_type', 'user_name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'phone_number': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required=False for all fields except phone_number and password
        for field_name in self.fields:
            if field_name not in ['phone_number', 'password']:
                self.fields[field_name].required = False

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    """For Login of the user"""
    email_or_phone = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')

        user = None
        # Check if the input is an email address or phone number
        if '@' in email_or_phone:
            user = authenticate(email=email_or_phone, password=password)
        else:
            user = authenticate(phone_number=email_or_phone, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials')
        
        if not user.is_active:
            raise AuthenticationFailed('User account is not active')

        data['user'] = user
        return data