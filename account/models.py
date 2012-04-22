from django.contrib.auth.models import User, Permission

from django.db import models
from django.dispatch.dispatcher import receiver

from core.models import BaseResource
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


class Profile(BaseResource):
    objects = ProfileManager()

    user = models.ForeignKey('auth.User')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.username

'''
class ResourcePermission(models.Model):

    person = models.ForeignKey(Profile)
    permission = models.ForeignKey(Permission)
    resource_pk = models.
'''