from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model, authenticate
import jwt
from django.conf import settings
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
import jwt
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

class CreateUserView(CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

class ManageUserView(RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    def get(self, request, *args, **kwargs):
        """Handle GET requests to retrieve user details."""
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests to update user details."""
        return self.partial_update(request, *args, **kwargs)

class UserDetailsView(RetrieveAPIView):
    """Retrieve details of the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
    
    
class LoginAPI(GenericAPIView):
    """Login API"""

    serializer_class = LoginSerializer  

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email_or_phone = serializer.validated_data['email_or_phone']
        password = serializer.validated_data['password']

        user = None
        # Check if the input is an email address or phone number
        if '@' in email_or_phone:
            user = authenticate(request, email=email_or_phone, password=password)
        else:
            user = authenticate(request, phone_number=email_or_phone, password=password)

        if user is not None:
            # Generate JWT token
            access_token = AccessToken.for_user(user)
            token = str(access_token)

            # Decode token to retrieve payload
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            return Response({
                'message': 'Login successful',
                'access_token': token,
                'payload': decoded_payload,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

