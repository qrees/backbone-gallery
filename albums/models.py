from django.db import models

# Create your models here.
from core.models import TimestampedModel

class Album(models.Model, TimestampedModel):
    name = models.CharField(max_length=255)
