from django.db import models
from django.contrib.auth.models import User


# Create your models here.


#https://www.youtube.com/watch?v=UxTwFMZ4r5k

class Drink(models.Model):
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

    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='images/')
    ingrediens = models.TextField()
    instructon = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    taste_type = models.CharField(max_length=10, choices=TASTE_CHOICES, default='sweet')
    strength = models.CharField(max_length=15, choices=STRENGTH_CHOICES, default='non-alcoholic')
    temperature = models.CharField(max_length=10, choices=TEMPERATURE_CHOICES, default='cold')
    complexity = models.CharField(max_length=10, choices=COMPLEXITY_CHOICES, default='simple')

    short_url = models.CharField(max_length=255, default="")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserVote(models.Model):
    VOTE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    vote_type = models.CharField(choices=VOTE_CHOICES, max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'drink'], name='unique_user_drink_vote')
        ]
