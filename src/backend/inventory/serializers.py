from rest_framework import serializers
from ..base.serializers import ModelSerializer
from .models import BookCategory, BookProduct, Approval
from ..accounts.serializers import UserSerializer
from datetime import datetime


class BookCategorySerializer(ModelSerializer):
    parent_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = BookCategory
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get("name", None)
        slug = validated_data.get("slug", None)
        if not slug:
            validated_data['slug'] = '_'.join(name.split())
        else:
            validated_data['slug'] = '_'.join(slug.split())
        instance = BookCategory.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        name = validated_data.get("name", None)
        slug = validated_data.get("slug", None)
        if not slug:
            validated_data['slug'] = '_'.join(name.split())
        else:
            validated_data['slug'] = '_'.join(slug.split())
        BookCategory.objects.filter(id=instance.pk, is_active=True).update(**validated_data)
        instance = BookCategory.objects.get(id=instance.pk)
        instance.save()
        return instance

    @staticmethod
    def get_parent_data(obj):
        return BookCategorySerializer(obj.parent).data if obj.parent else None


class BookProductSerializer(ModelSerializer):
    owner_data = serializers.SerializerMethodField(required=False)
    category_data = serializers.SerializerMethodField(required=False)
    total_price = serializers.SerializerMethodField(required=False)

    class Meta:
        model = BookProduct
        fields = '__all__'

    def validate(self, data):
        unit = data.get("unit", None)
        unit_price = data.get("unit_price", None)
        book_category = data.get('book_category', None)
        if not unit:
            raise serializers.ValidationError({'detail': ['Unit Field Required!']})
        if not unit_price:
            raise serializers.ValidationError({'detail': 'Unit Price Field Required!'})
        if not book_category:
            raise serializers.ValidationError({'detail': 'Book Category Field required!'})
        return data

    def create(self, validated_data):
        name = validated_data.get("name", None)
        slug = validated_data.get("slug", None)
        if not slug:
            validated_data['slug'] = '_'.join(name.split())
        else:
            validated_data['slug'] = '_'.join(slug.split())
        instance = BookProduct.objects.create(**validated_data)
        approval_data = {
            'approval_req': instance,
            'is_active': True
        }
        appr = Approval.objects.create(**approval_data)
        return instance

    def update(self, instance, validated_data):
        name = validated_data.get("name", None)
        slug = validated_data.get("slug", None)
        if not slug:
            validated_data['slug'] = '_'.join(name.split())
        else:
            validated_data['slug'] = '_'.join(slug.split())
        BookProduct.objects.filter(id=instance.pk, is_active=True).update(**validated_data)
        instance = BookProduct.objects.get(id=instance.pk)
        instance.save()
        return instance

    @staticmethod
    def get_owner_data(obj):
        return UserSerializer(obj.owner).data if obj.owner else None

    @staticmethod
    def get_category_data(obj):
        return BookCategorySerializer(obj.book_category).data if obj.book_category else None

    @staticmethod
    def get_total_price(obj):
        return obj.unit * obj.unit_price if obj.unit and obj.unit_price else None


class ApprovalSerializer(ModelSerializer):
    approval_req_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Approval
        fields = '__all__'

    def update(self, instance, validated_data):
        is_approved = validated_data.get('is_approved', None)
        is_rejected = validated_data.get('is_rejected', None)
        if is_approved:
            book_data: BookProduct.objects.filter(id=instance.approval_req.pk, is_active=True).first()
            book_data.is_approved: True
            book_data.is_rejected: False
            book_data.save()

        if is_rejected:
            book_data: BookProduct.objects.filter(id=instance.approval_req.pk, is_active=True).first()
            book_data.is_approved: False
            book_data.is_rejected: True
            book_data.save()

        validated_data["date"] = datetime.now()
        Approval.objects.filter(id=instance.pk, is_active=True).update(**validated_data)
        instance = Approval.objects.get(id=instance.pk)
        instance.save()
        return instance
