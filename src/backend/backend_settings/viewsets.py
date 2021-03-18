from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, JSONParser
from ..base.api.pagination import StandardResultsSetPagination
from rest_framework.decorators import action
from ..base.api.viewsets import ModelViewSet
from .serializers import SettingsSerializers
from .permissions import SettingsPermissions
from .models import Settings
from .constans import SETTINGS_CONSTANT
from .services import dropdown_tree
from ..base import response



class SettingsViewSet(ModelViewSet):
    serializer_class = SettingsSerializers
    permission_classes = (SettingsPermissions,)
    queryset = Settings.objects.all()

    @action(methods=['GET'], detail=False)
    def dropdown(self, request):
        dropdown_list = SETTINGS_CONSTANT
        data = dropdown_tree(dropdown_list, SettingsSerializers, Settings)
        return response.Ok(data)

