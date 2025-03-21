from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#https://www.youtube.com/watch?v=UxTwFMZ4r5k
class Drink(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='images/')
    ingrediens = models.TextField()
    instructon = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
