from django import forms

class ContactForm(forms.Form):
    username = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Email address')
    mobile_no = forms.CharField(max_length=15, label='Mobile No.')
    message = forms.CharField(widget=forms.Textarea, label='Message') 