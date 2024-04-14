from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Order
from Product.models import Product, Color, Size
from Payment.models import Payment

from django.contrib.auth import get_user_model

User = get_user_model()


class OrderSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(), write_only=True
    )

    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(), write_only=True
    )

    color_id = serializers.PrimaryKeyRelatedField(
        source='color',
        queryset=Color.objects.all(), write_only=True
    )

    size_id = serializers.PrimaryKeyRelatedField(
        source='size',
        queryset=Size.objects.all(), write_only=True
    )

    payment_id = serializers.PrimaryKeyRelatedField(
        source='payment',
        queryset=Payment.objects.all(), write_only=True
    )

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1
