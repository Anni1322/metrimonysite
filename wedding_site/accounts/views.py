from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token  # Use this for token authentication


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

# from .EmailService import EmailService


from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .serializers import (
    RegistrationSerializer, ProfileSerializer, 
    PreferencesSerializer, PhotoSerializer, LocationSerializer, UserSerializer
)
from .models import Profile, Preferences, Locations, Photos

User = get_user_model()

# --- Authentication/Registration Views ---
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    """
    POST: /api/register/
    Creates a new User account. Returns the user data and a new token.
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Automatically create Token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        # No need to manually create Profile/Preferences here; let get_or_create in detail views handle it with defaults
        
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key,
            "message": "Registration successful. Use this token for subsequent requests."
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    POST: /api/login/
    Authenticates user and returns an authentication token.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate using email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Login the user (optional, but good for session-based APIs)
            login(request, user)
            
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user_id": user.id,
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # Create a one-time use security token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # The URL user will click in their email (pointing to your React app)
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

            # Send Email
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n{reset_link}',
                'noreply@yourapp.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Reset link sent to your email"}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            # We return 200 even if user doesn't exist for security (prevents email leaking)
            return Response({"message": "If an account exists, a reset link was sent."}, status=status.HTTP_200_OK)
 

class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get("password")
        if not password:
            return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Check if token is valid for this user
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


# --- Core User Data Views ---

class EntryProfileView(APIView):
    permission_classes = [AllowAny]  # Allows access without token

    def post(self, request):
        email = request.data.get("email")
        
        if not email:
            return Response({"email": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Find the user by email
            user = User.objects.get(email=email)
            
            # 2. Get existing profile or create one
            profile, created = Profile.objects.get_or_create(user=user)
            
            # 3. Clean the data (handle empty date string from React)
            data = request.data.copy()
            if data.get('date_of_birth') == '':
                data.pop('date_of_birth')

            # 4. Serialize and Save
            serializer = ProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"email": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
                
        
        
class ProfileListView(generics.ListAPIView):
    """
    GET: /api/profiles/
    Returns a list of all public profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny] # Or IsAuthenticated
    

@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: /api/profile/ (Retrieve current user's profile)
    PUT/PATCH: /api/profile/ (Update current user's profile)
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure we are getting the profile associated with the authenticated user
        # Provide defaults for required fields to avoid errors
        profile, created = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'first_name': '',
                'last_name': '',
                'gender': 'other',
                'marital_status': 'single',
            }
        )
        return profile

class PreferencesDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: /api/preferences/ (Retrieve current user's preferences)
    PUT/PATCH: /api/preferences/ (Update current user's preferences)
    """
    serializer_class = PreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure we are getting the preferences associated with the authenticated user
        # Provide defaults for required fields
        preferences, created = Preferences.objects.get_or_create(
            user=self.request.user,
            defaults={
                'preferred_gender': 'other',
                'min_age': 18,
                'max_age': 100,
                'max_distance_km': 50,
            }
        )
        return preferences

# --- Photos List/Create View ---
class PhotoListView(generics.ListCreateAPIView):
    """
    GET: /api/photos/ (List all photos for the current user)
    POST: /api/photos/ (Upload a new photo)
    """
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter photos to only show those belonging to the current user
        return Photos.objects.filter(user=self.request.user).order_by('-is_primary', '-uploaded_at')

    def perform_create(self, serializer):
        # Set the user field automatically upon creation
        serializer.save(user=self.request.user)

# --- Locations View ---

class LocationDetailView(generics.RetrieveUpdateAPIView):
    """
    GET: /api/location/ (Retrieve current user's location)
    PUT/PATCH: /api/location/ (Update current user's location)
    """
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure we are getting the location associated with the authenticated user
        location, created = Locations.objects.get_or_create(user=self.request.user)
        return location