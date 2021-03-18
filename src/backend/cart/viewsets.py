from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, JSONParser
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from .serializers import CartSerializer
from .permissions import CartPermission
from .models import Cart


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (CartPermission,)
    queryset = Cart.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(CartViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = None
        queryset = self.filter_queryset(queryset)
        return queryset
