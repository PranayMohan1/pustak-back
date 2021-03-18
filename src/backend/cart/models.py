from django.db import models
from ..base.models import TimeStampedModel
from django.contrib.auth import get_user_model
from ..inventory.models import BookProduct

class Cart(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), related_name='customer', blank=True, null=True,
                              on_delete=models.PROTECT)
    book = models.ForeignKey(BookProduct, related_name='books', blank=True, null=True,
                                        on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
