from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile

class ContactForm(forms.Form):
    username = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Email address')
    mobile_no = forms.CharField(max_length=15, label='Mobile No.')
    message = forms.CharField(widget=forms.Textarea, label='Message')

class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    address = forms.CharField(widget=forms.Textarea)
    mobile = forms.CharField(max_length=15)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password'] 