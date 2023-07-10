from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user_details = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True)
    image_type = models.CharField(max_length=5, blank=True, null=True)
    gender = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now_add = True, blank=True, null=True)
