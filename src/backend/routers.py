from .accounts.viewsets import UserViewSet
from .base.api.routers import PustakRouter
from .inventory.viewsets import BookCategoryViewSet, BookProductViewSet
from .backend_settings.viewsets import SettingsViewSet

restricted_router = PustakRouter()

# Auth App
restricted_router.register(r'users', UserViewSet, basename='v1_auth')
restricted_router.register(r'category', BookCategoryViewSet, basename='v1_category')
restricted_router.register(r'product', BookProductViewSet, basename='v1_product')
restricted_router.register(r'settings', SettingsViewSet, basename='v1_setting')
