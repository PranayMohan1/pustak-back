from django.db import models

from ..base.models import TimeStampedModel
from django.contrib.auth import get_user_model


class BookCategory(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    slug = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=1024, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class BookProduct(TimeStampedModel):
    name = models.CharField(max_length=1024, blank=True, null=True)
    slug = models.CharField(max_length=1024, blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), related_name='book_owner', blank=True, null=True,
                              on_delete=models.PROTECT)
    book_category = models.ForeignKey(BookCategory, blank=True, null=True, on_delete=models.PROTECT),
    # publisher 
    # publication_year=models.DateField(blank=True, null=True),
    # author_name=models.CharField(blank=True, null=True),
    # language=models.CharField(blank=True, null=True),
    # book_type new book /use book
    desc = models.TextField(blank=True, null=True)
    short_desc = models.CharField(max_length=1024, blank=True, null=True)
    image = models.CharField(max_length=1024, blank=True, null=True)
    unit = models.IntegerField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)


class Approval(TimeStampedModel):
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    approved_by = models.ForeignKey(get_user_model(), related_name='approved_by', blank=True, null=True, on_delete=models.PROTECT)
    book = models.ForeignKey(BookProduct, blank=True, null=True, on_delete=models.PROTECT)
    remarks = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)
