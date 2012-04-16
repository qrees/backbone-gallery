from django.contrib.auth.models import User
from django.db import models
from django.dispatch.dispatcher import receiver

from core.utils import gen_uuid

from social_auth.signals import socialauth_registered

@receiver(socialauth_registered)
def social_user_registered(sender, user, response, details, **kwargs):
    profile = Profile.objects.create(user=user, email=details['email'], username=details['username'])


class ProfileManager(models.Manager):

    def create_account(self, password, **kwargs):
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