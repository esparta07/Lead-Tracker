from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.contrib.auth.hashers import check_password
from .models import User
import jwt
from leadapp import settings


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data.get('email_or_phone')
            try:
                # Attempt to find the user by email
                user = User.objects.get(email=email_or_phone)
            except User.DoesNotExist:
                try:
                    # If the user is not found by email, attempt to find by phone number
                    user = User.objects.get(phone_number=email_or_phone)
                except User.DoesNotExist:
                    # If user is not found by email or phone number, return error
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if check_password(serializer.validated_data['password'], user.password):
                payload = {
                    'user_id': user.pk,
                    'username': user.user_name,
                    'email': user.email,
                    'role': user.get_role(),
                    'full_name': user.full_name,
                    'user_type': user.user_type,
                }
                # Update payload with token-specific information (expiration, issued at, etc.) if needed
                access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                request.session['access_token'] = access_token
                return Response({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'payload':payload,
                }, status=status.HTTP_200_OK)
            else:
                # Incorrect password
                return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid serializer data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)