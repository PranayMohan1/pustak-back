
from django.db import models
from ..base.models import TimeStampedModel


class Settings(TimeStampedModel):
    name=models.CharField(max_length=1024,blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=1024, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)