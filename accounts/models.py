from typing import BinaryIO
import votes
from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(auth.models.User, auth.models.PermissionsMixin):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return "@{}".format(self.get_username())

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    image = models.FileField(upload_to="static/images", null=True, blank=True)
    votes = models.IntegerField(default=0)
    token = models.CharField(null=True, blank=True, default=0, max_length=30)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.user.name



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
