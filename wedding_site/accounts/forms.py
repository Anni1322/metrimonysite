from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']