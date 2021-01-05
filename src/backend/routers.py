from .accounts.viewsets import UserViewSet
from .base.api.routers import PustakRouter

restricted_router = PustakRouter()

# Auth App
restricted_router.register(r'users', UserViewSet, basename='v1_auth')