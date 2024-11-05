from typing import Any
from django.contrib.auth.models import User
from django.db import models

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    # is_online = models.BooleanField(default=False)
    profile_picture_url = models.URLField(null=True, blank=True)
    intra_id = models.IntegerField(null=True, blank=True)
    suitColor = models.CharField(max_length=7, default='')
    visColor = models.CharField(max_length=7, default='')
    ringsColor = models.CharField(max_length=7, default='')
    bpColor = models.CharField(max_length=7, default='')
    # twoFA_code = models.CharField(max_length=6, default='')
    twoFA_enabled = models.BooleanField(default=False)
    # twoFA_code_expiration = models.DateTimeField(null=True, blank=True)
    # twoFA_verified = models.BooleanField(default=False)
    friends_list = models.ManyToManyField("self", blank=True)
    flatness = models.FloatField(default=2.8)
    horizontalPosition = models.FloatField(default=0.73)
    verticalPosition = models.FloatField(default=0.08)


    def __str__(self):
        return f"{self.user.username} (ID: {self.user.id}, IntraID: {self.intra_id})" # pour debug
