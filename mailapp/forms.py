from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message, Contact

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ComposeForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email']