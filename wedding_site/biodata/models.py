from django.db import models
import datetime

from django.contrib.auth import get_user_model
from django.conf import settings

# 3. Reference the User model like this
User = get_user_model()

class CommunityBiodata(models.Model):
    
    
    
    # Choices
    GENDER_CHOICES = [('M', 'Male/पुरुष'), ('F', 'Female/महिला'), ('O', 'Other/अन्य')]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('Unmarried', 'अविवाहित (Unmarried)'),
        ('Married', 'विवाहित (Married)'),
        ('Divorced', 'तलाकशुदा (Divorced)'),
        ('Widow/Widower', 'विधवा/विधुर (Widow/Widower)'),
    ]

    # --- Meta Information ---
    # serial_number is now blank=True, editable=False so it's managed by the system
    serial_number = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="सरल क्रमांक (Serial Number)",
        editable=False, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय है? (Is Active)")

    # --- Profile Media ---
    profile_photo = models.ImageField(upload_to='biodata_photos/', verbose_name="फोटो (Photo)", blank=True, null=True)

    # --- Personal Details ---
    full_name = models.CharField(max_length=255, verbose_name="नाम (Name)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="लिंग (Gender)", null=True)
    date_of_birth = models.DateField(verbose_name="जन्मतिथि (Date of Birth)")
    birth_time = models.TimeField(verbose_name="जन्म समय (Birth Time)", blank=True, null=True)
    birth_place = models.CharField(max_length=255, verbose_name="जन्म स्थान (Birth Place)", blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, verbose_name="रक्त समूह (Blood Group)", blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='Unmarried', verbose_name="वैवाहिक स्थिति (Marital Status)")

    # --- Community Specifics ---
    caste = models.CharField(max_length=100, verbose_name="जाति (Caste)", default="Gond")
    gotra = models.CharField(max_length=100, verbose_name="गोत्र (Gotra)")
    deity_number = models.CharField(max_length=50, verbose_name="देव संख्या (Deity Number)")
    
    # --- Family Details ---
    father_name = models.CharField(max_length=255, verbose_name="पिता का नाम (Father's Name)")
    father_occupation = models.CharField(max_length=255, verbose_name="पिता का व्यवसाय", blank=True)
    mother_name = models.CharField(max_length=255, verbose_name="माता का नाम (Mother's Name)")
    maternal_uncle_gotra = models.CharField(max_length=100, verbose_name="मामा का गोत्र (Mama Gotra)")
    family_status = models.TextField(verbose_name="पारिवारिक स्थिति (Family Status)", help_text="भाई-बहन की जानकारी")

    # --- Physical Attributes ---
    complexion = models.CharField(max_length=50, verbose_name="रंग (Complexion)")
    height = models.CharField(max_length=20, verbose_name="कद (Height)")
    weight = models.PositiveIntegerField(verbose_name="वजन (Weight in kg)", blank=True, null=True) # NEW

    # --- Professional & Educational ---
    education = models.TextField(verbose_name="शिक्षा (Education)")
    occupation = models.CharField(max_length=255, verbose_name="वर्तमान व्यवसाय", default="निरंक")
    work_location = models.CharField(max_length=255, verbose_name="कार्य स्थल (Work Location)", blank=True) # NEW
    annual_income = models.CharField(max_length=100, verbose_name="वार्षिक आय (Annual Income)", blank=True)

    # --- Contact & Address ---
    address = models.TextField(verbose_name="पूरा पता (Address)")
    city = models.CharField(max_length=100, verbose_name="शहर/ग्राम (City/Village)", blank=True)
    district = models.CharField(max_length=100, verbose_name="जिला (District)", blank=True)
    state = models.CharField(max_length=100, verbose_name="राज्य (State)", default="Chhattisgarh") # NEW
    guardian_mobile = models.CharField(max_length=15, verbose_name="पालक का मोबाईल (Guardian Mobile)")
    candidate_mobile = models.CharField(max_length=15, verbose_name="स्वयं का मोबाईल (Candidate Mobile)", blank=True)
    email = models.EmailField(verbose_name="ईमेल (Email)", blank=True) # NEW

    user = models.OneToOneField(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE, 
            related_name="community_profile",  # Change this from "profile" to "community_profile"
            null=True, 
            blank=True,
            verbose_name="यूजर अकाउंट"
        )


    # --- Logic for Automatic Serial Number ---
    # def save(self, *args, **kwargs):
    #     if not self.serial_number:
    #         # Logic: BIO-2024-0001
    #         year = datetime.date.today().year
    #         last_record = CommunityBiodata.objects.all().order_by('id').last()
    #         if not last_record:
    #             new_id = 1
    #         else:
    #             new_id = last_record.id + 1
    #         self.serial_number = f"BIO-{year}-{new_id:04d}"
    #     super(CommunityBiodata, self).save(*args, **kwargs)
    
    
    
    def save(self, *args, **kwargs):
            if not self.serial_number:
                import datetime
                year = datetime.date.today().year
                last_record = CommunityBiodata.objects.all().order_by('id').last()
                new_id = 1 if not last_record else last_record.id + 1
                self.serial_number = f"BIO-{year}-{new_id:04d}"
            super(CommunityBiodata, self).save(*args, **kwargs)    


    def __str__(self):
        return f"{self.serial_number} - {self.full_name}"

    class Meta:
        verbose_name = "Biodata Profile"
        verbose_name_plural = "Biodata Profiles"
        ordering = ['-created_at']
       
       
        
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
        
        
        

  