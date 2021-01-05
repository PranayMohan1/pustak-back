from rest_framework.authentication import TokenAuthentication

from ..accounts.models import AuthTokenModel


class SportTokenAuthentication(TokenAuthentication):
    model = AuthTokenModel
