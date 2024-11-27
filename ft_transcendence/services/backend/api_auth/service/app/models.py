from django.contrib.auth.models import User
from django.db import models

class CustomUserModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    profile_picture_url = models.URLField(default='/images/default.jpg')
    intra_id = models.IntegerField(null=True, blank=True)
    suitColor = models.CharField(max_length=7, default='#ffffff')
    visColor = models.CharField(max_length=7, default='#e48d2d')
    ringsColor = models.CharField(max_length=7, default='#ffffff')
    bpColor = models.CharField(max_length=7, default='#ffffff')
    twoFA_enabled = models.BooleanField(default=False)
    friends_list = models.ManyToManyField("self", blank=True)
    flatness = models.FloatField(default=2.8)
    horizontalPosition = models.FloatField(default=7.5)
    verticalPosition = models.FloatField(default=0)
