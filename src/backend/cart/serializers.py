from ..base.serializers import ModelSerializer
from .models import Cart


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
