from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, JSONParser
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from .serializers import SettingsSerializers
from .permissions import SettingsPermissions
from .models import Settings

class SettingsViewSet(ModelViewSet):
    serializer_class = SettingsSerializers
    permission_classes = (SettingsPermissions,)
    queryset = Settings.objects.all()

