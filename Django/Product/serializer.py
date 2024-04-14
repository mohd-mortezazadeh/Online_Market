from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

from Category.models import Category

class ImageSerializer(ModelSerializer):
    image = serializers.ImageField(required=False , use_url=True)
    class Meta:
        model = Image
        fields = '__all__'

    read_only_fields = [
        "created_at",
        "updated_at",
    ]


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

    read_only_fields = [
        "created_at",
        "updated_at",
    ]


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

    read_only_fields = [
        "created_at",
        "updated_at",
    ]



class SuggestSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.filter(block_status=False), write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.filter(status=True), write_only=True
    )

    class Meta:
        model = Suggest
        fields = '__all__'
        depth = 1

    read_only_fields = [
        "created_at",
        "updated_at",
    ]


class ProductSerializer(ModelSerializer):
    original_image = serializers.ImageField(required=False, use_url=True)
    images = ImageSerializer(many=True , read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    #################################
    color_id = serializers.PrimaryKeyRelatedField(
        many=True,
        source='colors',
        queryset=Color.objects.all() , write_only=True
    )

    size_id = serializers.PrimaryKeyRelatedField(
        many=True,
        source='sizes',
        queryset=Size.objects.all(), write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

        read_only_fields = [
            "created_at",
            "updated_at",
        ]



class NotifyUserSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = NotifyUser
        fields = '__all__'
        depth = 1

        read_only_fields = [
            "created_at",
            "updated_at",
        ]