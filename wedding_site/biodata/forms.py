from django import forms
from .models import CommunityBiodata

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border-gray-200 rounded-xl py-3 px-4 mb-4',
                'placeholder': f'Enter {field.label}'
            })




from django import forms
from .models import CommunityBiodata

class CommunityBiodataForm(forms.ModelForm):
    class Meta:
        model = CommunityBiodata
        fields = '__all__'
        widgets = {
            # Date and Time
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'birth_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            
            # Textareas
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'family_status': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),

            # --- Dropdowns (Use forms.Select for choices to work) ---
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'caste': forms.Select(attrs={'class': 'form-control'}),
            'gotra': forms.Select(attrs={'class': 'form-control'}),
            'complexion': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.Select(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'occupation': forms.Select(attrs={'class': 'form-control'}),
            'father_occupation': forms.Select(attrs={'class': 'form-control'}),
            'annual_income': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),


            # --- Standard Text Inputs ---
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_place': forms.TextInput(attrs={'class': 'form-control'}),
            'deity_number': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'maternal_uncle_gotra': forms.TextInput(attrs={'class': 'form-control'}),
            'work_location': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'candidate_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
            # File Input Styling
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }












# class CommunityBiodataForm(forms.ModelForm):
#     class Meta:
#         model = CommunityBiodata
#         fields = '__all__'
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'education': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
#             'family_status': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            
#             # Text Inputs
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'caste': forms.TextInput(attrs={'class': 'form-control'}),
#             'gotra': forms.TextInput(attrs={'class': 'form-control'}),
#             'deity_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'father_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'maternal_uncle_gotra': forms.TextInput(attrs={'class': 'form-control'}),
#             'complexion': forms.TextInput(attrs={'class': 'form-control'}),
#             'height': forms.TextInput(attrs={'class': 'form-control'}),
#             'occupation': forms.TextInput(attrs={'class': 'form-control'}),
#             'guardian_mobile': forms.TextInput(attrs={'class': 'form-control'}),
#             'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            
#             # File Input Styling
#             'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#         }
        
        
        
        
        
        










# from django import forms
# from .models import CommunityBiodata

# class CommunityBiodataForm(forms.ModelForm):
#     class Meta:
#         model = CommunityBiodata
#         fields = '__all__'
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'education': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
#             'family_status': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            
#             # Text Inputs
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'caste': forms.TextInput(attrs={'class': 'form-control'}),
#             'gotra': forms.TextInput(attrs={'class': 'form-control'}),
#             'deity_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'father_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'maternal_uncle_gotra': forms.TextInput(attrs={'class': 'form-control'}),
#             'complexion': forms.TextInput(attrs={'class': 'form-control'}),
#             'height': forms.TextInput(attrs={'class': 'form-control'}),
#             'occupation': forms.TextInput(attrs={'class': 'form-control'}),
#             'guardian_mobile': forms.TextInput(attrs={'class': 'form-control'}),
#             'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            
#             # File Input Styling
#             'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#         }
        
        
        
        
        















# from django import forms
# from .models import CommunityBiodata

# class CommunityBiodataForm(forms.ModelForm):
#     class Meta:
#         model = CommunityBiodata
#         fields = '__all__'
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'education': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
#             'family_status': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
#             # Apply standard class to all text inputs
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'caste': forms.TextInput(attrs={'class': 'form-control'}),
#             'gotra': forms.TextInput(attrs={'class': 'form-control'}),
#             'deity_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'father_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'maternal_uncle_gotra': forms.TextInput(attrs={'class': 'form-control'}),
#             'complexion': forms.TextInput(attrs={'class': 'form-control'}),
#             'height': forms.TextInput(attrs={'class': 'form-control'}),
#             'occupation': forms.TextInput(attrs={'class': 'form-control'}),
#             'guardian_mobile': forms.TextInput(attrs={'class': 'form-control'}),
#             'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }
        
        


# from django import forms
# from .models import CommunityBiodata

# class CommunityBiodataForm(forms.ModelForm):
#     class Meta:
#         model = CommunityBiodata
#         fields = '__all__'
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'education': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
#             'family_status': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
#         }
#         labels = {
#             # Labels are already defined in models.py verbose_name, 
#             # but you can override them here if needed.
#         }

#     def __init__(self, *args, **kwargs):
#         super(CommunityBiodataForm, self).__init__(*args, **kwargs)
#         # Optional: Add Bootstrap/CSS classes to all fields loop
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})