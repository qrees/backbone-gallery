from django.contrib.auth.models import User
from django.db import models

from core.utils import gen_uuid


class ProfileManager(models.Manager):

    def create(self, password, **kwargs):
        user = User.objects.create_user(username=gen_uuid(), password=password)
        profile = super(ProfileManager, self).create(user=user, **kwargs)
        return profile


class Profile(models.Model):
    objects = ProfileManager()

    user = models.ForeignKey('auth.User')
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.username