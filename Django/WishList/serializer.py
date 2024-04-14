from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from Product.models import Product
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()

class WishlistSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.filter(block_status=False), write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.filter(status=True), write_only=True
    )

    class Meta:
        model = Wishlist
        fields = '__all__'
        depth = 1