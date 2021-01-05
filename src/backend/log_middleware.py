from datetime import datetime

import pandas as pd
from django.conf import settings
from django.db.models.signals import *
from django.dispatch import receiver
from django.http import JsonResponse
from django.utils import timezone

from .accounts.models import User, AuthTokenModel


class LogAllMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global user_id
        user_id = None
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            token = token[6:]
            user_obj = AuthTokenModel.objects.filter(key=token).first()
            if user_obj and (timezone.now() - pd.to_datetime(
                    user_obj.last_accessed)).total_seconds() > settings.INACTIVITY_LOGOUT_TIME_SECONDS:
                user_obj.delete()
                return JsonResponse({'detail': 'Session Expired due to inactivity'}, status=401)
            elif user_obj:
                user_id = user_obj.user
                user_obj.last_accessed = datetime.now()
                user_obj.save()
        return self.get_response(request)

    @receiver(pre_save)
    def add_creator(sender, instance, **kwargs):
        if not instance.pk and hasattr(instance, 'created_by') and user_id:
            instance.created_by = User.objects.get(email=user_id)
        return instance
