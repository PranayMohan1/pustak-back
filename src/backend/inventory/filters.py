import django_filters
from .models import BookCategory, BookProduct, Approval


class BookCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = BookCategory
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'parent': ['exact']
        }


class BookProductFilter(django_filters.FilterSet):
    class Meta:
        model = BookProduct
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'owner': ['exact'],
            'book_categories': ['exact'],
            'unit_price': ['exact'],
            'unit': ['exact']
        }


class ApprovalFilter(django_filters.FilterSet):
    class Meta:
        model = Approval
        fields = {
            'id': ['exact'],
            'is_approved': ['exact'],
            'is_rejected': ['exact'],
            'approved_by': ['exact'],
            # 'book': ['exact', 'icontains'],
        }
