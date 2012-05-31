from django.db import models

from account.models import Profile
from core.models import TimestampedModelMixin, BaseResource


class Album(TimestampedModelMixin, BaseResource):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile)

    def as_dict(self):
        d = super(Album, self).as_dict()
        return d


class File(TimestampedModelMixin, BaseResource):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='photos/%Y/%m/%d')
    album = models.ForeignKey(Album)
