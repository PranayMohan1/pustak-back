from rest_framework import serializers
from ..base.serializers import ModelSerializer
from .models import Settings


class SettingsSerializers(ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'

