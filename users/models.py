from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile/%y/%m/%d', blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    cv = models.TextField()
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    linkdin = models.URLField(null=True,blank=True)
    def get_absolute_url(self):
        username = User.get_username
        return reverse('user:author_info', args=[self.username])