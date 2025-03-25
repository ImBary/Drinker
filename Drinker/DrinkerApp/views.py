from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import DrinkPreferenceForm
from .forms import DrinkForm, RegisterForm
from .models import Drink
import pyshorteners
from django.http import HttpResponse


def home(request):
    drinks = Drink.objects.all()
    return render(request, "home.html", {"drinks": drinks})


@login_required()
def add_drink(request):
    if request.method == "POST":
        form = DrinkForm(request.POST, request.FILES)
        if form.is_valid():
            drink = form.save(commit=False)
            drink.user = request.user
            drink.save()

            url = request.build_absolute_uri(f"/drink/{drink.id}")

            # Short URL
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(url)
            drink.short_url = short_url

            # Save
            drink.save()
            return redirect("home")
    else:
        form = DrinkForm()
    return render(request, "add_drink.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home")


def recommend_drink(request):
    recommended_drink = None
    matches=[]
    if request.method == "POST":
        form = DrinkPreferenceForm(request.POST)
        if form.is_valid():
            taste = form.cleaned_data['taste']
            strength = form.cleaned_data['strength']
            temperature = form.cleaned_data['temperature']
            complexity = form.cleaned_data['complexity']
            isInBase = False

            drinks = Drink.objects.all()
            if taste:
                filtred = drinks.filter(taste_type__icontains=taste)
                if filtred.exists():
                    drinks = filtred
                    matches.append("taste")
                    isInBase=True
            if strength:
                filtred = drinks.filter(strength__icontains=strength)
                if filtred.exists():
                    drinks = filtred
                    matches.append("strength")
                    isInBase=True
            if temperature:
                filtred = drinks.filter(temperature__icontains=temperature)
                if filtred.exists():
                    drinks = filtred
                    matches.append("temperature")
                    isInBase=True
            if complexity:
                filtred = drinks.filter(complexity__icontains = complexity)
                if filtred.exists():
                    drinks = filtred
                    matches.append("complexity")
                    isInBase=True
            if drinks.exists() and isInBase:
                recommended_drink = drinks.order_by('?').first()
            else:
                messages.warning(request,"Sorry, we dont have this type of drink in our base yet...")
                return render(request,'drink_recommendation.html',{'form':form})
                
    else:
        form = DrinkPreferenceForm()
    return render(request,'drink_recommendation.html',{'form':form, 'drink':recommended_drink, 'matches':matches})


def drink_view(request, drink_id):
    drink = Drink.objects.filter(id=drink_id).first()
    ingredients_list = drink.ingrediens.split(',')
    return render(request, "drink_view.html", {'drink': drink, 'ingredients_list': ingredients_list})
