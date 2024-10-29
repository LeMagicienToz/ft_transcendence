from django.contrib.auth.models import User
from django.db import models

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    profile_picture_url = models.URLField(null=True, blank=True)
    intra_id = models.IntegerField(null=True, blank=True)
    suitColor = models.CharField(max_length=7, default='')
    visColor = models.CharField(max_length=7, default='')
    ringsColor = models.CharField(max_length=7, default='')
    bpColor = models.CharField(max_length=7, default='')

    def __str__(self):
        return f"{self.user.username} (ID: {self.user.id}, IntraID: {self.intra_id})" # pour debug
