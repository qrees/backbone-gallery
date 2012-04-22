from django.db import models

from account.models import Profile
from core.models import TimestampedModelMixin, BaseResource


class Album(TimestampedModelMixin, BaseResource):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile)
