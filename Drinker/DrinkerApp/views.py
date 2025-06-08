from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import DrinkPreferenceForm
from .forms import DrinkForm, RegisterForm
from .models import Drink, UserVote
import pyshorteners
from django.http import HttpResponse
import os
from PIL import Image
import numpy as np
import tensorflow as tf
from django import forms

MODEL_PATH = os.path.join('DrinkerApp', 'ml_model', 'model.h5')
drink_model = tf.keras.models.load_model(MODEL_PATH)


def home(request):
    drinks = Drink.objects.all()
    paginator = Paginator(drinks, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"drinks": page_obj})


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
    matches = []
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
                    isInBase = True
            if strength:
                filtred = drinks.filter(strength__icontains=strength)
                if filtred.exists():
                    drinks = filtred
                    matches.append("strength")
                    isInBase = True
            if temperature:
                filtred = drinks.filter(temperature__icontains=temperature)
                if filtred.exists():
                    drinks = filtred
                    matches.append("temperature")
                    isInBase = True
            if complexity:
                filtred = drinks.filter(complexity__icontains=complexity)
                if filtred.exists():
                    drinks = filtred
                    matches.append("complexity")
                    isInBase = True
            if drinks.exists() and isInBase:
                recommended_drink = drinks.order_by('?').first()
            else:
                messages.warning(request, "Sorry, we dont have this type of drink in our base yet...")
                return render(request, 'drink_recommendation.html', {'form': form})

    else:
        form = DrinkPreferenceForm()
    return render(request, 'drink_recommendation.html', {'form': form, 'drink': recommended_drink, 'matches': matches})


def drink_view(request, drink_id):
    drink = Drink.objects.filter(id=drink_id).first()
    ingredients_list = drink.ingrediens.split(',')
    return render(request, "drink_view.html", {'drink': drink, 'ingredients_list': ingredients_list})


@login_required
def like_drink(request, drink_id):
    drink = Drink.objects.filter(id=drink_id).first()

    user_vote = UserVote.objects.filter(user=request.user, drink=drink).first()

    if user_vote:
        if user_vote.vote_type == 'like':
            messages.warning(request, "Zostalo juz polikowane")
        else:
            drink.dislikes -= 1
            drink.likes += 1
            user_vote.vote_type = 'like'
            user_vote.save()
            drink.save()
    else:
        drink.likes += 1
        UserVote.objects.create(user=request.user, drink=drink, vote_type='like')
        drink.save()

    return redirect(request.POST.get("next", "home"))


@login_required
def dislike_drink(request, drink_id):
    drink = Drink.objects.filter(id=drink_id).first()

    user_vote = UserVote.objects.filter(user=request.user, drink=drink).first()

    if user_vote:
        if user_vote.vote_type == 'dislike':
            messages.warning(request, "Zostalo juz zdislikowane")
        else:
            drink.likes -= 1
            drink.dislikes += 1
            user_vote.vote_type = 'dislike'
            user_vote.save()
            drink.save()
    else:
        drink.dislikes += 1
        UserVote.objects.create(user=request.user, drink=drink, vote_type='dislike')
        drink.save()

    return redirect(request.POST.get("next", "home"))


@login_required
def update_drink(request, drink_id):
    drink = Drink.objects.filter(id=drink_id).first()

    if request.method == 'POST':
        form = DrinkForm(request.POST, request.FILES, instance=drink)
        if form.is_valid():
            form.save()
            messages.success(request, "Drink został zaktualizowany.")
            return redirect('home')
    else:
        form = DrinkForm(instance=drink)

    return render(request, 'update_drink.html', {'form': form, 'drink': drink})


@login_required
def delete_drink(request, drink_id):
    drink = Drink.objects.filter(id=drink_id).first()

    if request.method == 'POST':
        drink.delete()
        messages.success(request, "Drink został usunięty.")
        return redirect('home')

    return render(request, 'delete_drink.html', {'drink': drink})

def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_500(request):
    return render(request, "errors/500.html", status=500)

def predict_drink(image_file):
    image = Image.open(image_file).convert('RGB')
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = drink_model.predict(img_array)
    class_index = np.argmax(predictions)

    class_names = ['amaretto_sour', 'aperol_spritz', 'bloody_mary', 'caiprinha', 'cosmopolitan', 'daiquiri', 'french_75', 'gin_fizz', 'long_island_ice_tea', 'mai_tai', 'margarita', 'martini', 'mint_julep', 'mojito', 'negroni', 'old_fashioned', 'pina_colada', 'whiskey_sour', 'white_russian']
    return class_names[class_index]



class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Upload an image")


@login_required
def drink_recognition(request):
    prediction = None

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            prediction = predict_drink(image)
        else:
            messages.error(request, "Invalid form submission. Please try again.")
    else:
        form = ImageUploadForm()

    return render(request, 'drink_recognition.html', {
        'form': form,
        'prediction': prediction
    })
