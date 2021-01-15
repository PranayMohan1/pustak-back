from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, JSONParser
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from .serializers import BookCategorySerializer, BookProductSerializer, ApprovalSerializer
from .models import BookCategory, BookProduct, Approval
from .filters import BookCategoryFilter, BookProductFilter, ApprovalFilter
from .permissions import BookCategoryPermissions, BookProductPermissions
from rest_framework.decorators import action
from ..base import response
from ..base.services import create_update_record


class BookCategoryViewSet(ModelViewSet):
    serializer_class = BookCategorySerializer
    queryset = BookCategory.objects.all()
    permission_classes = (BookCategoryPermissions,)
    parser_classes = (JSONParser, MultiPartParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(BookCategoryViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = BookCategoryFilter
        queryset = self.filter_queryset(queryset)
        return queryset


class BookProductViewSet(ModelViewSet):
    serializer_class = BookProductSerializer
    queryset = BookProduct.objects.all()
    permission_classes = (BookProductPermissions,)
    parser_classes = (JSONParser, MultiPartParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(BookProductViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = BookProductFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(methods=['GET', 'POST'], detail=False)
    def book_approval(self, request):
        if request.method == "GET":
            queryset = Approval.objects.filter(is_active=True)
            self.filterset_class = ApprovalFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return response.Ok(self.get_paginated_response(page).data)
            return response.Ok(ApprovalSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, ApprovalSerializer, Approval))
