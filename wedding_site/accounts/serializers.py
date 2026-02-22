# # your_app_name/serializers.py

# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import Profile, Preferences, Locations, Photos

# User = get_user_model()

# # --- User Registration/Login ---

# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for the User model (used for reading data)."""
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'role')
#         read_only_fields = ('role',)

# class RegistrationSerializer(serializers.ModelSerializer):
#     """Serializer for User registration (handles password hashing)."""
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password2')
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         # Note: Since USERNAME_FIELD is 'email', Django's User model
#         # often auto-sets the username from the email if not provided.
#         # We manually set it here for compatibility:
#         data['username'] = data['email'] 
#         return data

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             username=validated_data['email'], # Use email as username
#             password=validated_data['password']
#         )
#         # Handle the password_hash field which you included in your model
#         # Django automatically handles hashing, so this field might be redundant.
#         # If it's intended to store the hash, Django's User.password field is used.
#         return user

# # --- Profile and Preferences ---

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         # Exclude 'user' as it's set automatically by the view
#         exclude = ('user',) 

# class PreferencesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Preferences
#         exclude = ('user',)

# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photos
#         fields = ('id', 'photo_url', 'is_primary', 'uploaded_at')
#         read_only_fields = ('uploaded_at',)

# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Locations
#         exclude = ('user', 'updated_at')





from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Preferences, Locations, Photos

User = get_user_model()

# --- User Registration/Login ---

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model (used for reading data)."""
    class Meta:
        model = User
        fields = ('id', 'email', 'role')
        read_only_fields = ('role',)

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for User registration (handles password hashing)."""
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # Note: Since USERNAME_FIELD is 'email', Django's User model
        # often auto-sets the username from the email if not provided.
        # We manually set it here for compatibility:
        data['username'] = data['email'] 
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],  # Use email as username
            password=validated_data['password']
        )
        # Handle the password_hash field which you included in your model
        # Django automatically handles hashing, so this field might be redundant.
        # If it's intended to store the hash, Django's User.password field is used.
        return user

# --- Profile and Preferences ---

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         # Exclude 'user' as it's set automatically by the view
#         exclude = ('user',) 

 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # Exclude 'user' from fields because we set it automatically in the view
        fields = [
            'id', 'first_name', 'last_name', 'gender', 'date_of_birth', 
            'height', 'religion', 'caste', 'occupation', 'education', 
            'income_range', 'marital_status', 'about_me', 'interests', 
            'profile_picture_url', 'is_verified'
        ]
        read_only_fields = ['is_verified'] # Only admins should verify
        
        


class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        exclude = ('user',)
        
        
        
        

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ('id', 'photo_url', 'is_primary', 'uploaded_at')
        read_only_fields = ('uploaded_at',)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        exclude = ('user', 'updated_at')