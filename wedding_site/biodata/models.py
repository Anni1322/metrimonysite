import datetime
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Validator for Mobile Numbers
phone_validator = RegexValidator(
    regex=r'^\d{10,15}$',
    message="Mobile number must be between 10 to 15 digits."
)

class CommunityBiodata(models.Model):
    # --- Choice Definitions (Keep your existing lists here) ---
    GENDER_CHOICES = [('M', 'Male/पुरुष'), ('F', 'Female/महिला')]
    BLOOD_GROUP_CHOICES = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')]
    MARITAL_STATUS_CHOICES = [('Unmarried', 'अविवाहित (Unmarried)'), ('Divorced', 'तलाकशुदा (Divorced)')]
    COMPLEXION_CHOICES = [('Fair', 'गोरा (Fair)'), ('Wheatish', 'सावला (Wheatish)'), ('Dark', 'काला (Dark)')]
    WEIGHT_CHOICES = [('Underweight', 'कम वजन (50 किग्रा से कम)'), ('Average', 'मध्यम वजन (50 – 70 किग्रा)'), ('Overweight', 'अधिक वजन (70 किग्रा से अधिक)')]
    HEIGHT_CHOICES = [(f"{ft}'{inch}\"", f"{ft} फीट {inch} इंच") for ft in range(4, 7) for inch in range(12)] + [('7\'0"', '7 फीट')]
    EDUCATION_CHOICES = [('Primary', 'प्रारंभिक शिक्षा'), ('12th', '12वीं (बारहवीं)'), ('Graduation', 'स्नातक (Graduation)'), ('PG', 'स्नातकोत्तर (PG)'), ('Other', 'अन्य (Other)')]
    OCCUPATION_CHOICES = [('Agriculture', 'कृषि (Agri)'), ('Job', 'नौकरी (Naukri)'), ('Business', 'व्यवसाय (Business)'), ('Other', 'अन्य (Anya)')]
    INCOME_CHOICES = [('Low', 'कम आय (₹7000 से कम)'), ('Medium', 'मध्यम आय (₹7000 – ₹20,000)'), ('High', 'अधिक आय (₹20,000 से अधिक)')]
    STATE_CHOICES = [('Chhattisgarh', 'Chhattisgarh (छत्तीसगढ़)'), ('Other', 'Other (अन्य)')]
    
    
    
    DISTRICT_CHOICES = [
        ('Balod', 'Balod (बालोद)'), ('Baloda Bazar', 'Baloda Bazar (बलौदा बाजार)'), ('Balrampur', 'Balrampur (बालरामपुर)'),
        ('Bastar', 'Bastar (बस्तर)'), ('Bemetara', 'Bemetara (बेमेतरा)'), ('Bijapur', 'Bijapur (बीजापुर)'),
        ('Bilaspur', 'Bilaspur (बिलासपुर)'), ('Dantewada', 'Dantewada (दंतेवाड़ा)'), ('Dhamtari', 'Dhamtari (धमतरी)'),
        ('Durg', 'Durg (दुर्ग)'), ('Gariaband', 'Gariaband (गरियाबंद)'), ('Janjgir-Champa', 'Janjgir-Champa (जांजगीर-चांपा)'),
        ('Korba', 'Korba (कोरबा)'), ('Raigarh', 'Raigarh (रायगढ़)'), ('Raipur', 'Raipur (रायपुर)'), ('Other', 'Other (अन्य)')
    ]

  
    CASTE_CHOICES = [
        ('Agariya', 'अगरिया'), ('Andh', 'अंध'), ('Baiga', 'बैगा'), ('Baina', 'बैना'),
        ('Bharia', 'भारिया भूमिया'), ('Bhattra', 'भतरा'), ('Bhil', 'भील'),
        ('Bhunjia', 'भुंजिया'), ('Gond', 'गोंड'), ('Halba', 'हल्बा'),
        ('Kawar', 'कंवर'), ('Khairwar', 'खैरवार'), ('Kharia', 'खड़िया'),
        ('Kol', 'कोल'), ('Korku', 'कोरकू'), ('Korwa', 'कोरवा'),
        ('Nagesia', 'नगेसिया'), ('Oraon', 'उरांव'), ('Pao', 'पाव'),
        ('Pardhan', 'परधान'), ('Saharaiya', 'सहरिया'), ('Sawar', 'सावरा'),
    ]

    GOTRA_CHOICES = [
        ('Nag', 'नाग (Nag)'), ('Bagh', 'बाघ (Bagh)'), ('Kachhua', 'कछुआ (Kachhua)'),
        ('Hans', 'हंस (Hans)'), ('Bhaisa', 'भैंसा (Bhaisa)'), ('Karait', 'करैत (Karait)'),
        ('Netam', 'नेताम (Netam)'), ('Markam', 'मरकाम (Markam)'), ('Tekam', 'टेकाम (Tekam)'),
        ('Lakra', 'लकरा (Lakra)'), ('Minj', 'मिंज (Minj)'), ('Tirkey', 'तिर्की (Tirkey)'),
        ('Ekka', 'एक्का (Ekka)'), ('Kujur', 'कुजूर (Kujur)'), ('Toppo', 'टोप्पो (Toppo)'),
        ('Prahlad', 'प्रहलाद (Prahlad)'), ('Vashishtha', 'वशिष्ठ (Vashishtha)'),
        ('Kasyap', 'कश्यप (Kasyap)'),
    ]






    # --- Fields ---
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User Account",editable=False)
    
    serial_number = models.CharField(max_length=50, unique=True, verbose_name="सरल क्रमांक", editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name="सक्रिय है?", editable=False)

    full_name = models.CharField(max_length=255, verbose_name="पूरा नाम (Full Name)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="लिंग (Gender)", null=True)
    date_of_birth = models.DateField(verbose_name="जन्मतिथि (Date of Birth)")
    birth_time = models.TimeField(verbose_name="जन्म समय (Birth Time)", blank=True, null=True)
    birth_place = models.CharField(max_length=255, verbose_name="जन्म स्थान (Birth Place)", blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, verbose_name="रक्त समूह", blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='Unmarried', verbose_name="वैवाहिक स्थिति")
    profile_photo = models.ImageField(upload_to='biodata_photos/', verbose_name="फोटो (Photo)", blank=True, null=True)
    caste = models.CharField(max_length=100, choices=CASTE_CHOICES, verbose_name="जाति (Caste)", default="Gond")
    gotra = models.CharField(max_length=100, choices=GOTRA_CHOICES, verbose_name="गोत्र (Gotra)")
    deity_number = models.CharField(max_length=50, verbose_name="देव संख्या (Deity Number)")
    father_name = models.CharField(max_length=255, verbose_name="पिता का नाम")
    mother_name = models.CharField(max_length=255, verbose_name="माता का नाम")
    maternal_uncle_gotra = models.CharField(max_length=100, verbose_name="मामा का गोत्र (Mama Gotra)")
    family_status = models.TextField(verbose_name="पारिवारिक स्थिति", help_text="भाई-बहन की जानकारी")
    height = models.CharField(max_length=20, choices=HEIGHT_CHOICES, verbose_name="कद (Height)", blank=True, null=True)
    education = models.CharField(max_length=100, choices=EDUCATION_CHOICES, verbose_name="शिक्षा (Education)", null=True, blank=True)
    occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, verbose_name="वर्तमान व्यवसाय", default="Other")
    address = models.TextField(verbose_name="पूरा पता")
    guardian_mobile = models.CharField(max_length=15, validators=[phone_validator], verbose_name="पालक का मोबाईल")
    candidate_mobile = models.CharField(max_length=15, validators=[phone_validator], verbose_name="स्वयं का मोबाईल", blank=True)
    email = models.EmailField(verbose_name="ईमेल", blank=True)
    
    state = models.CharField(max_length=100, choices=STATE_CHOICES, verbose_name="राज्य", default="Chhattisgarh")
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, verbose_name="जिला", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="शहर/ग्राम", blank=True)
    address = models.TextField(verbose_name="पूरा पता")  
    
    
    city = models.CharField(max_length=100, verbose_name="शहर/ग्राम", blank=True, null=True) # Add this
    
    
    def clean(self):
        super().clean()
        if self.date_of_birth:
            if self.date_of_birth > datetime.date.today():
                raise ValidationError({'date_of_birth': "Date of birth cannot be in the future."})
            age = (datetime.date.today() - self.date_of_birth).days // 365
            if age < 18:
                raise ValidationError({'date_of_birth': "Candidate must be at least 18 years old."})

    def save(self, *args, **kwargs):
        if not self.serial_number:
            year = datetime.date.today().year
            count = CommunityBiodata.objects.filter(created_at__year=year).count() + 1
            self.serial_number = f"BIO-{year}-{count:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.serial_number} - {self.full_name}"













# from django.db import models
# import datetime

# from django.contrib.auth import get_user_model
# from django.conf import settings

# # 3. Reference the User model like this
# User = get_user_model()


# from django.core.exceptions import ValidationError
# from django.core.validators import RegexValidator

# # Validator for Mobile Numbers
# phone_validator = RegexValidator(
#     regex=r'^\d{10,15}$',
#     message="Mobile number must be between 10 to 15 digits."
# )

# class CommunityBiodata(models.Model):
#     # --- Choice Definitions ---
#     GENDER_CHOICES = [('M', 'Male/पुरुष'), ('F', 'Female/महिला')]
    
#     BLOOD_GROUP_CHOICES = [
#         ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
#         ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
#     ]
    
#     MARITAL_STATUS_CHOICES = [
#         ('Unmarried', 'अविवाहित (Unmarried)'),
#         ('Divorced', 'तलाकशुदा (Divorced)')
#     ]

#     COMPLEXION_CHOICES = [
#         ('Fair', 'गोरा (Fair)'),
#         ('Wheatish', 'सावला (Wheatish)'),
#         ('Dark', 'काला (Dark)'),
#     ]

#     WEIGHT_CHOICES = [
#         ('Underweight', 'कम वजन (50 किग्रा से कम)'),
#         ('Average', 'मध्यम वजन (50 – 70 किग्रा)'),
#         ('Overweight', 'अधिक वजन (70 किग्रा से अधिक)'),
#     ]

#     # Dynamically generate height from 4'0" to 7'0"
#     HEIGHT_CHOICES = [(f"{ft}'{inch}\"", f"{ft} फीट {inch} इंच") for ft in range(4, 7) for inch in range(12)] + [('7\'0"', '7 फीट')]

#     EDUCATION_CHOICES = [
#         ('Primary', 'प्रारंभिक शिक्षा'),
#         ('12th', '12वीं (बारहवीं)'),
#         ('Graduation', 'स्नातक (Graduation)'),
#         ('PG', 'स्नातकोत्तर (PG)'),
#         ('Other', 'अन्य (Other)'),
#     ]

#     OCCUPATION_CHOICES = [
#         ('Agriculture', 'कृषि (Agri)'),
#         ('Job', 'नौकरी (Naukri)'),
#         ('Business', 'व्यवसाय (Business)'),
#         ('Other', 'अन्य (Anya)'),
#     ]

#     INCOME_CHOICES = [
#         ('Low', 'कम आय (₹7000 से कम)'),
#         ('Medium', 'मध्यम आय (₹7000 – ₹20,000)'),
#         ('High', 'अधिक आय (₹20,000 से अधिक)'),
#     ]

#     STATE_CHOICES = [
#         ('Chhattisgarh', 'Chhattisgarh (छत्तीसगढ़)'),
#         ('Other', 'Other (अन्य)'),
#     ]

#     DISTRICT_CHOICES = [
#         ('Balod', 'Balod (बालोद)'), ('Baloda Bazar', 'Baloda Bazar (बलौदा बाजार)'),
#         ('Balrampur', 'Balrampur (बालरामपुर)'), ('Bastar', 'Bastar (बस्तर)'),
#         ('Bemetara', 'Bemetara (बेमेतरा)'), ('Bijapur', 'Bijapur (बीजापुर)'),
#         ('Bilaspur', 'Bilaspur (बिलासपुर)'), ('Dantewada', 'Dantewada (दंतेवाड़ा)'),
#         ('Dhamtari', 'Dhamtari (धमतरी)'), ('Durg', 'Durg (दुर्ग)'),
#         ('Gariaband', 'Gariaband (गरियाबंद)'), ('Gaurela-Pendra-Marwahi', 'Gaurela-Pendra-Marwahi (गौरेला-पेंड्रा-मरवाही)'),
#         ('Janjgir-Champa', 'Janjgir-Champa (जांजगीर-चांपा)'), ('Jashpur', 'Jashpur (जशपुर)'),
#         ('Kabirdham', 'Kabirdham (कबीरधाम)'), ('Kanker', 'Kanker (कांकेर)'),
#         ('Kondagaon', 'Kondagaon (कोंडागांव)'), ('Korba', 'Korba (कोरबा)'),
#         ('Korea', 'Korea (कोरिया)'), ('Mahasamund', 'Mahasamund (महासमुंद)'),
#         ('Manendragarh-Chirmiri-Bharatpur', 'Manendragarh-Chirmiri-Bharatpur (मनेंद्रगढ़-चिरमिरी-भरतपुर)'),
#         ('Mohla-Manpur-Ambagarh Chowki', 'Mohla-Manpur-Ambagarh Chowki (मोहला-मानपुर-अंबागढ़ चौकी)'),
#         ('Mungeli', 'Mungeli (मुंगेली)'), ('Narayanpur', 'Narayanpur (नारायणपुर)'),
#         ('Raigarh', 'Raigarh (रायगढ़)'), ('Raipur', 'Raipur (रायपुर)'),
#         ('Rajnandgaon', 'Rajnandgaon (राजनांदगांव)'), ('Sakti', 'Sakti (सक्ती)'),
#         ('Sarangarh-Bilaigarh', 'Sarangarh-Bilaigarh (सारंगढ़-बिलाईगढ़)'), ('Sukma', 'Sukma (सुकमा)'),
#         ('Surajpur', 'Surajpur (सूरजपुर)'), ('Surguja', 'Surguja (सरगुजा)'),
#         ('Khairagarh-Chhuikhadan-Gandai', 'Khairagarh-Chhuikhadan-Gandai (खैरागढ़-छुईखदान-गंडई)'),
#         ('Other', 'Other (अन्य)'),
#     ]

#     CASTE_CHOICES = [
#         ('Agariya', 'अगरिया'), ('Andh', 'अंध'), ('Baiga', 'बैगा'), ('Baina', 'बैना'),
#         ('Bharia', 'भारिया भूमिया'), ('Bhattra', 'भतरा'), ('Bhil', 'भील'),
#         ('Bhunjia', 'भुंजिया'), ('Gond', 'गोंड'), ('Halba', 'हल्बा'),
#         ('Kawar', 'कंवर'), ('Khairwar', 'खैरवार'), ('Kharia', 'खड़िया'),
#         ('Kol', 'कोल'), ('Korku', 'कोरकू'), ('Korwa', 'कोरवा'),
#         ('Nagesia', 'नगेसिया'), ('Oraon', 'उरांव'), ('Pao', 'पाव'),
#         ('Pardhan', 'परधान'), ('Saharaiya', 'सहरिया'), ('Sawar', 'सावरा'),
#     ]

#     GOTRA_CHOICES = [
#         ('Nag', 'नाग (Nag)'), ('Bagh', 'बाघ (Bagh)'), ('Kachhua', 'कछुआ (Kachhua)'),
#         ('Hans', 'हंस (Hans)'), ('Bhaisa', 'भैंसा (Bhaisa)'), ('Karait', 'करैत (Karait)'),
#         ('Netam', 'नेताम (Netam)'), ('Markam', 'मरकाम (Markam)'), ('Tekam', 'टेकाम (Tekam)'),
#         ('Lakra', 'लकरा (Lakra)'), ('Minj', 'मिंज (Minj)'), ('Tirkey', 'तिर्की (Tirkey)'),
#         ('Ekka', 'एक्का (Ekka)'), ('Kujur', 'कुजूर (Kujur)'), ('Toppo', 'टोप्पो (Toppo)'),
#         ('Prahlad', 'प्रहलाद (Prahlad)'), ('Vashishtha', 'वशिष्ठ (Vashishtha)'),
#         ('Kasyap', 'कश्यप (Kasyap)'),
#     ]

#     # --- Meta Information ---
#     serial_number = models.CharField(max_length=50, unique=True, verbose_name="सरल क्रमांक", editable=False, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True, verbose_name="सक्रिय है?" ,editable=False)

#     # --- Personal Details ---
#     full_name = models.CharField(max_length=255, verbose_name="पूरा नाम (Full Name)")
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="लिंग (Gender)", null=True)
#     date_of_birth = models.DateField(verbose_name="जन्मतिथि (Date of Birth)")
#     birth_time = models.TimeField(verbose_name="जन्म समय (Birth Time)", blank=True, null=True)
#     birth_place = models.CharField(max_length=255, verbose_name="जन्म स्थान (Birth Place)", blank=True)
#     blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, verbose_name="रक्त समूह", blank=True)
#     marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='Unmarried', verbose_name="वैवाहिक स्थिति")

#     # --- Profile Media ---
#     profile_photo = models.ImageField(upload_to='biodata_photos/', verbose_name="फोटो (Photo)", blank=True, null=True)

#     # --- Community Specifics ---
#     caste = models.CharField(max_length=100, choices=CASTE_CHOICES, verbose_name="जाति (Caste)", default="Gond")
#     gotra = models.CharField(max_length=100, choices=GOTRA_CHOICES, verbose_name="गोत्र (Gotra)")
#     deity_number = models.CharField(max_length=50, verbose_name="देव संख्या (Deity Number)")
    
#     # --- Family Details ---
#     father_name = models.CharField(max_length=255, verbose_name="पिता का नाम")
#     father_occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, verbose_name="पिता का व्यवसाय", blank=True, null=True)
#     mother_name = models.CharField(max_length=255, verbose_name="माता का नाम")
#     maternal_uncle_gotra = models.CharField(max_length=100, verbose_name="मामा का गोत्र (Mama Gotra)")
#     family_status = models.TextField(verbose_name="पारिवारिक स्थिति", help_text="भाई-बहन की जानकारी")

#     # --- Physical Attributes ---
#     complexion = models.CharField(max_length=50, choices=COMPLEXION_CHOICES, verbose_name="रंग (Complexion)", blank=True, null=True)
#     height = models.CharField(max_length=20, choices=HEIGHT_CHOICES, verbose_name="कद (Height)", blank=True, null=True)
#     weight = models.CharField(max_length=50, choices=WEIGHT_CHOICES, verbose_name="वजन (Weight)", blank=True, null=True)

#     # --- Professional & Educational ---
#     education = models.CharField(max_length=100, choices=EDUCATION_CHOICES, verbose_name="शिक्षा (Education)", null=True, blank=True)
#     occupation = models.CharField(max_length=100, choices=OCCUPATION_CHOICES, verbose_name="वर्तमान व्यवसाय", default="Other")
#     work_location = models.CharField(max_length=255, verbose_name="कार्य स्थल", blank=True)
#     annual_income = models.CharField(max_length=100, choices=INCOME_CHOICES, verbose_name="वार्षिक आय", blank=True, null=True)

#     # --- Contact & Address ---
#     state = models.CharField(max_length=100, choices=STATE_CHOICES, verbose_name="राज्य", default="Chhattisgarh")
#     district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, verbose_name="जिला", blank=True, null=True)
#     city = models.CharField(max_length=100, verbose_name="शहर/ग्राम", blank=True)
#     address = models.TextField(verbose_name="पूरा पता")

#     guardian_mobile = models.CharField(max_length=15, validators=[phone_validator], verbose_name="पालक का मोबाईल")
#     candidate_mobile = models.CharField(max_length=15, validators=[phone_validator], verbose_name="स्वयं का मोबाईल", blank=True)
#     email = models.EmailField(verbose_name="ईमेल", blank=True)
    
    
#     user = models.ForeignKey(
#             settings.AUTH_USER_MODEL, 
#             on_delete=models.CASCADE, 
#             null=True, 
#             blank=True,
#             verbose_name="User Account"
#         )   
        

#     def clean(self):
#         """Custom validation logic"""
#         super().clean()
        
#         # 1. Validate Date of Birth (Should not be in the future)
#         if self.date_of_birth and self.date_of_birth > datetime.date.today():
#             raise ValidationError({'date_of_birth': "Date of birth cannot be in the future."})

#         # 2. Minimum Age Validation (e.g., 18 years for marriage biodata)
#         if self.date_of_birth:
#             age = (datetime.date.today() - self.date_of_birth).days // 365
#             if age < 18:
#                 raise ValidationError({'date_of_birth': "Candidate must be at least 18 years old."})

#         # 3. Ensure candidate and guardian mobile numbers are different (Optional)
#         if self.candidate_mobile and self.guardian_mobile:
#             if self.candidate_mobile == self.guardian_mobile:
#                 raise ValidationError({'candidate_mobile': "Candidate mobile should be different from Guardian mobile."})

#     def save(self, *args, **kwargs):
#         # Call full_clean to trigger the clean() method before saving
#         self.full_clean()
        
#         if not self.serial_number:
#             year = datetime.date.today().year
#             count = CommunityBiodata.objects.count() + 1
#             self.serial_number = f"BIO-{year}-{count:04d}"
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.serial_number} - {self.full_name}"

#     class Meta:
#         verbose_name = "Biodata Profile"
#         verbose_name_plural = "Biodata Profiles"
#         ordering = ['-created_at']





















# class CommunityBiodata(models.Model):
#     # Choices
#     GENDER_CHOICES = [('M', 'Male/पुरुष'), ('F', 'Female/महिला'), ('O', 'Other/अन्य')]
#     BLOOD_GROUP_CHOICES = [
#         ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
#         ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
#     ]
#     MARITAL_STATUS_CHOICES = [
#         ('Unmarried', 'अविवाहित (Unmarried)'),
#         ('Divorced', 'तलाकशुदा (Divorced)')
#     ]

#     # --- Meta Information ---
#     # serial_number is now blank=True, editable=False so it's managed by the system
#     serial_number = models.CharField(
#         max_length=50, 
#         unique=True, 
#         verbose_name="सरल क्रमांक (Serial Number)",
#         editable=False, 
#         blank=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True, verbose_name="सक्रिय है? (Is Active)")

#     # --- Profile Media ---
#     profile_photo = models.ImageField(upload_to='biodata_photos/', verbose_name="फोटो (Photo)", blank=True, null=True)

#     # --- Personal Details ---
#     full_name = models.CharField(max_length=255, verbose_name="नाम (Name)")
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="लिंग (Gender)", null=True)
#     date_of_birth = models.DateField(verbose_name="जन्मतिथि (Date of Birth)")
#     birth_time = models.TimeField(verbose_name="जन्म समय (Birth Time)", blank=True, null=True)
#     birth_place = models.CharField(max_length=255, verbose_name="जन्म स्थान (Birth Place)", blank=True)
#     blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, verbose_name="रक्त समूह (Blood Group)", blank=True)
#     marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='Unmarried', verbose_name="वैवाहिक स्थिति (Marital Status)")

#     # --- Community Specifics ---
#     caste = models.CharField(max_length=100, verbose_name="जाति (Caste)", default="Gond")
#     gotra = models.CharField(max_length=100, verbose_name="गोत्र (Gotra)")
#     deity_number = models.CharField(max_length=50, verbose_name="देव संख्या (Deity Number)")
    
#     # --- Family Details ---
#     father_name = models.CharField(max_length=255, verbose_name="पिता का नाम (Father's Name)")
#     father_occupation = models.CharField(max_length=255, verbose_name="पिता का व्यवसाय", blank=True)
#     mother_name = models.CharField(max_length=255, verbose_name="माता का नाम (Mother's Name)")
#     maternal_uncle_gotra = models.CharField(max_length=100, verbose_name="मामा का गोत्र (Mama Gotra)")
#     family_status = models.TextField(verbose_name="पारिवारिक स्थिति (Family Status)", help_text="भाई-बहन की जानकारी")

#     # --- Physical Attributes ---
#     complexion = models.CharField(max_length=50, verbose_name="रंग (Complexion)")
#     height = models.CharField(max_length=20, verbose_name="कद (Height)")
#     weight = models.PositiveIntegerField(verbose_name="वजन (Weight in kg)", blank=True, null=True) # NEW

#     # --- Professional & Educational ---
#     education = models.TextField(verbose_name="शिक्षा (Education)")
#     occupation = models.CharField(max_length=255, verbose_name="वर्तमान व्यवसाय", default="निरंक")
#     work_location = models.CharField(max_length=255, verbose_name="कार्य स्थल (Work Location)", blank=True) # NEW
#     annual_income = models.CharField(max_length=100, verbose_name="वार्षिक आय (Annual Income)", blank=True)

#     # --- Contact & Address ---
#     address = models.TextField(verbose_name="पूरा पता (Address)")
#     city = models.CharField(max_length=100, verbose_name="शहर/ग्राम (City/Village)", blank=True)
#     district = models.CharField(max_length=100, verbose_name="जिला (District)", blank=True)
#     state = models.CharField(max_length=100, verbose_name="राज्य (State)", default="Chhattisgarh") # NEW
#     guardian_mobile = models.CharField(max_length=15, verbose_name="पालक का मोबाईल (Guardian Mobile)")
#     candidate_mobile = models.CharField(max_length=15, verbose_name="स्वयं का मोबाईल (Candidate Mobile)", blank=True)
#     email = models.EmailField(verbose_name="ईमेल (Email)", blank=True) # NEW

#     user = models.OneToOneField(
#             settings.AUTH_USER_MODEL, 
#             on_delete=models.CASCADE, 
#             related_name="community_profile",  # Change this from "profile" to "community_profile"
#             null=True, 
#             blank=True,
#             verbose_name="यूजर अकाउंट"
#         )


#     # --- Logic for Automatic Serial Number ---
#     def save(self, *args, **kwargs):
#         if not self.serial_number:
#             # Logic: BIO-2024-0001
#             year = datetime.date.today().year
#             last_record = CommunityBiodata.objects.all().order_by('id').last()
#             if not last_record:
#                 new_id = 1
#             else:
#                 new_id = last_record.id + 1
#             self.serial_number = f"BIO-{year}-{new_id:04d}"
#         super(CommunityBiodata, self).save(*args, **kwargs)
    
    
    
#     def save(self, *args, **kwargs):
#             if not self.serial_number:
#                 import datetime
#                 year = datetime.date.today().year
#                 last_record = CommunityBiodata.objects.all().order_by('id').last()
#                 new_id = 1 if not last_record else last_record.id + 1
#                 self.serial_number = f"BIO-{year}-{new_id:04d}"
#             super(CommunityBiodata, self).save(*args, **kwargs)    


#     def __str__(self):
#         return f"{self.serial_number} - {self.full_name}"

#     class Meta:
#         verbose_name = "Biodata Profile"
#         verbose_name_plural = "Biodata Profiles"
#         ordering = ['-created_at']
       
       
        
class SuccessStory(models.Model):
    couple_name = models.CharField(max_length=255, verbose_name="जोड़े का नाम")
    wedding_date = models.DateField(verbose_name="शादी की तिथि")
    image = models.ImageField(upload_to='success_stories/', verbose_name="जोड़े की फोटो")
    story_text = models.TextField(verbose_name="सफलता की कहानी")
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.couple_name        
        
        


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="biodata_sent_messages"  # Changed this
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="biodata_received_messages"  # Changed this
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']



# from django.db import models

# class CommunityBiodata(models.Model):
#     # Meta Information
#     created_at = models.DateTimeField(auto_now_add=True)
#     serial_number = models.CharField(
#         max_length=50, 
#         unique=True,
#         verbose_name="सरल क्रमांक (Serial Number)"
#     )

#     # NEW: Image Field
#     profile_photo = models.ImageField(
#         upload_to='biodata_photos/', 
#         verbose_name="फोटो (Photo)", 
#         blank=True, 
#         null=True
#     )

#     # Personal Details
#     full_name = models.CharField(max_length=255, verbose_name="नाम (Name)")
#     caste = models.CharField(max_length=100, verbose_name="जाति (Caste)", default="Gond")
#     gotra = models.CharField(max_length=100, verbose_name="गोत्र (Gotra)")
#     deity_number = models.CharField(max_length=50, verbose_name="देव संख्या (Deity Number)")
    
#     # Family Details
#     father_name = models.CharField(max_length=255, verbose_name="पिता का नाम (Father's Name)")
#     mother_name = models.CharField(max_length=255, verbose_name="माता का नाम (Mother's Name)")
#     maternal_uncle_gotra = models.CharField(max_length=100, verbose_name="मामा का गोत्र (Mama Gotra)")
#     family_status = models.TextField(verbose_name="पारिवारिक स्थिति (Family Status)")

#     # Physical Attributes
#     complexion = models.CharField(max_length=50, verbose_name="रंग (Complexion)")
#     height = models.CharField(max_length=20, verbose_name="कद (Height)")
#     date_of_birth = models.DateField(verbose_name="जन्मतिथि (Date of Birth)")

#     # Professional & Educational
#     education = models.TextField(verbose_name="शिक्षा (Education)")
#     occupation = models.CharField(max_length=255, verbose_name="वर्तमान व्यवसाय", default="निरंक")

#     # Contact & Address
#     address = models.TextField(verbose_name="पूरा पता (Address)")
#     guardian_mobile = models.CharField(max_length=15, verbose_name="पालक का मोबाईल (Mobile)")

#     def __str__(self):
#         return f"{self.serial_number} - {self.full_name}"

#     class Meta:
#         verbose_name = "Biodata Profile"
#         verbose_name_plural = "Biodata Profiles"
#         ordering = ['-created_at']
        
        
        

  