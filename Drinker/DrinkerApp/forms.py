from django import forms
from .models import Drink
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Drinki
class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ["name", "description", "photo", "ingrediens", "instructon"]


# Rejestracja
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']