from django.db import models


class TimestampedModelMixin(object):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
