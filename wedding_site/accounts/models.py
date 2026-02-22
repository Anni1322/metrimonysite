# from django.db import models
# from django.contrib.auth.models import AbstractUser
# # from django.contrib.gis.db import models as gis_models
# from django.core.validators import MinValueValidator, MaxValueValidator

# class User(AbstractUser):
#     # Extends Django's AbstractUser; maps to Users table
#     email = models.EmailField(unique=True)
#     password_hash = models.CharField(max_length=255)  # Use Django's password field
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     ROLE_CHOICES = [('user', 'User'), ('admin', 'Admin'), ('vendor', 'Vendor')]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         db_table = 'Users'

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     date_of_birth = models.DateField()
#     height = models.DecimalField(max_digits=5, decimal_places=2)
#     religion = models.CharField(max_length=100)
#     caste = models.CharField(max_length=100)
#     occupation = models.CharField(max_length=255)
#     education = models.CharField(max_length=255)
#     income_range = models.CharField(max_length=100)
#     MARITAL_STATUS_CHOICES = [('single', 'Single'), ('divorced', 'Divorced'), ('widowed', 'Widowed')]
#     marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
#     about_me = models.TextField()
#     interests = models.TextField()
#     profile_picture_url = models.URLField(max_length=500, blank=True)
#     is_verified = models.BooleanField(default=False)

#     class Meta:
#         db_table = 'Profiles'

# class Preferences(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     PREFERRED_GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
#     preferred_gender = models.CharField(max_length=10, choices=PREFERRED_GENDER_CHOICES)
#     min_age = models.IntegerField(validators=[MinValueValidator(18)])
#     max_age = models.IntegerField(validators=[MaxValueValidator(100)])
#     preferred_religion = models.CharField(max_length=100)
#     preferred_caste = models.CharField(max_length=100)
#     preferred_occupation = models.CharField(max_length=255)
#     preferred_education = models.CharField(max_length=255)
#     preferred_income_range = models.CharField(max_length=100)
#     preferred_location = models.CharField(max_length=255)
#     max_distance_km = models.IntegerField()

#     class Meta:
#         db_table = 'Preferences'

# # class Locations(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     location = gis_models.PointField()  # GIS PointField for lat/long
# #     city = models.CharField(max_length=100)
# #     state = models.CharField(max_length=100)
# #     country = models.CharField(max_length=100)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     class Meta:
# #         db_table = 'Locations'


# class Locations(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     latitude = models.DecimalField(max_digits=10, decimal_places=8, validators=[MinValueValidator(-90), MaxValueValidator(90)])
#     longitude = models.DecimalField(max_digits=11, decimal_places=8, validators=[MinValueValidator(-180), MaxValueValidator(180)])
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = 'Locations'

# class Location_Preferences(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     preferred_city = models.CharField(max_length=100)
#     preferred_state = models.CharField(max_length=100)
#     preferred_country = models.CharField(max_length=100)
#     radius_km = models.IntegerField(default=50)

#     class Meta:
#         db_table = 'Location_Preferences'

# class Photos(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     photo_url = models.URLField(max_length=500)
#     is_primary = models.BooleanField(default=False)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'Photos'







from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# --- Custom Manager ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # Ensure username is not being passed if it's set to None in the model
        extra_fields.pop('username', None) 
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# --- Updated User Model ---
class User(AbstractUser):
    # 1. Remove the username field inherited from AbstractUser
    username = None 
    
    # 2. Use email as the primary identifier
    email = models.EmailField(unique=True)
    
    # 3. Add your custom fields
    ROLE_CHOICES = [('user', 'User'), ('admin', 'Admin'), ('vendor', 'Vendor')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Note: 'is_active', 'last_login', and 'password' are 
    # already included in AbstractUser. No need to redefine them.

    # 4. Configure Authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email and Password are required by default

    # 5. Attach the Manager
    objects = UserManager()

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.email












# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.core.validators import MinValueValidator, MaxValueValidator

# class User(AbstractUser):
#     # Extends Django's AbstractUser; maps to Users table
#     email = models.EmailField(unique=True)
#     password_hash = models.CharField(max_length=255)  # Redundant (Django handles passwords), but kept as per your code
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     ROLE_CHOICES = [('user', 'User'), ('admin', 'Admin'), ('vendor', 'Vendor')]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         db_table = 'Users'




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    date_of_birth = models.DateField(null=True, blank=True)  # Made optional
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Made optional
    religion = models.CharField(max_length=100, blank=True, default='')
    caste = models.CharField(max_length=100, blank=True, default='')
    occupation = models.CharField(max_length=255, blank=True, default='')
    education = models.CharField(max_length=255, blank=True, default='')
    income_range = models.CharField(max_length=100, blank=True, default='')
    MARITAL_STATUS_CHOICES = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')]
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='single')
    about_me = models.TextField(blank=True, default='')
    interests = models.TextField(blank=True, default='')
    profile_picture_url = models.URLField(max_length=500, blank=True, default='')
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'Profiles'



class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PREFERRED_GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    preferred_gender = models.CharField(max_length=10, choices=PREFERRED_GENDER_CHOICES, default='other')
    min_age = models.IntegerField(validators=[MinValueValidator(18)], default=18)
    max_age = models.IntegerField(validators=[MaxValueValidator(100)], default=100)
    preferred_religion = models.CharField(max_length=100, blank=True, default='')
    preferred_caste = models.CharField(max_length=100, blank=True, default='')
    preferred_occupation = models.CharField(max_length=255, blank=True, default='')
    preferred_education = models.CharField(max_length=255, blank=True, default='')
    preferred_income_range = models.CharField(max_length=100, blank=True, default='')
    preferred_location = models.CharField(max_length=255, blank=True, default='')
    max_distance_km = models.IntegerField(default=50)

    class Meta:
        db_table = 'Preferences'

class Locations(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=11, decimal_places=8, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Locations'

class Location_Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_city = models.CharField(max_length=100, blank=True, default='')
    preferred_state = models.CharField(max_length=100, blank=True, default='')
    preferred_country = models.CharField(max_length=100, blank=True, default='')
    radius_km = models.IntegerField(default=50)

    class Meta:
        db_table = 'Location_Preferences'

class Photos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_url = models.URLField(max_length=500)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Photos'