from django.db import models

# Create your models here.
from core.models import TimestampedModelMixin

class Album(models.Model, TimestampedModelMixin):
    name = models.CharField(max_length=255)
