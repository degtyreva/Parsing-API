
# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    address = models.TextField()
    phone = models.TextField()
    website = models.TextField()
    company = models.TextField()
    objects = models.Manager()
    def __str__(self):
        return self.name



class Post(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    body = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.title