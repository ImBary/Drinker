from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("add/", views.add_drink, name="add_drink"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recommend/', views.recommend_drink, name="drink_recommendation"),
    path('drink/<int:drink_id>', views.drink_view, name="drink_view"),
    path('like_drink/<int:drink_id>/', views.like_drink, name='like_drink'),
    path('dislike_drink/<int:drink_id>/', views.dislike_drink, name='dislike_drink'),
    path('drink/<int:drink_id>/edit/', views.update_drink, name='update_drink'),
    path('drink/<int:drink_id>/delete/', views.delete_drink, name='delete_drink'),
]
