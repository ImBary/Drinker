from django import forms
from .models import Drink
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Drinki
from django import forms
from .models import Drink

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ["name", "description", "photo", "ingrediens", "instructon", 
                  "taste_type", "strength", "temperature", "complexity"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "photo": forms.FileInput(attrs={"class": "form-control", "style": "display: block; width: 30%; padding: 0px;"}),  
            "ingrediens": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "instructon": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "taste_type": forms.Select(attrs={"class": "form-select"}),
            "strength": forms.Select(attrs={"class": "form-select"}),
            "temperature": forms.Select(attrs={"class": "form-select"}),
            "complexity": forms.Select(attrs={"class": "form-select"}),
        }

# Rejestracja
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

TASTE_CHOICES = [
        ('sweet', 'Sweet'),
        ('bitter', 'Bitter'),
        ('sour', 'Sour'),
        ('salty', 'Salty'),
        ('umami', 'Umami'),
    ]
    
STRENGTH_CHOICES = [
        ('non-alcoholic', 'Non-Alcoholic'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]
    
TEMPERATURE_CHOICES = [
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('warm', 'Warm'),
    ]
    
COMPLEXITY_CHOICES = [
        ('simple', 'Simple'),
        ('moderate', 'Moderate'),
        ('complex', 'Complex'),
    ]

class DrinkPreferenceForm(forms.Form):
    taste = forms.ChoiceField(choices=TASTE_CHOICES, widget=forms.RadioSelect, label="What taste do you prefer?")
    strength = forms.ChoiceField(choices=STRENGTH_CHOICES, widget=forms.RadioSelect, label="How strong should it be?")
    temperature = forms.ChoiceField(choices=TEMPERATURE_CHOICES, widget=forms.RadioSelect, label="Preferred temperature?")
    complexity = forms.ChoiceField(choices=COMPLEXITY_CHOICES, widget=forms.RadioSelect, label="How complex should it be?")
