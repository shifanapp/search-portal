# forms.py
from django import forms

class FreelancerRegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    username = forms.CharField(max_length=100, required=True, label="Username")
    email = forms.EmailField(required=True, label="E-mail")
    phone = forms.CharField(max_length=10, required=True, label="Phone No", 
                            widget=forms.TextInput(attrs={'pattern': '^\d{10}$', 'placeholder': 'Enter your phone number'}))
    whatsapp = forms.CharField(max_length=10, required=False, label="WhatsApp No", 
                               widget=forms.TextInput(attrs={'pattern': '^\d{10}$', 'placeholder': 'Enter your WhatsApp number'}))
    category = forms.ChoiceField(choices=[('', 'Select category'), ('Design', 'Design'), ('Development', 'Development'), ('Writing', 'Writing')], 
                                 required=True, label="Category")
    profile_photo = forms.ImageField(required=False, label="Profile Photo")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
    skills = forms.CharField(required=False, label="Skills")
