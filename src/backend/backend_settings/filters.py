import django_filters
from .models import Settings

class SettingsFilter(django_filters.FilterSet):
    class Meta:
        model=Settings
        fields={
            'id': ['exact'],
            'name': ['exact', 'icontains'],
        }
