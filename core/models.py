import uuid

from django.db import models


class TimestampedModelMixin(object):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


def gen_uuid():
    u = uuid.uuid4()
    return u.hex


class BaseResource(models.Model):
    uuid = models.CharField(max_length=32, default=gen_uuid, unique=True)

    class Meta:
        abstract = True
