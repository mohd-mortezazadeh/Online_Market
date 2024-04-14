from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class StarSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.filter(block_status=False), write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.filter(status=True), write_only=True
    )

    class Meta:
        model = Star
        fields = '__all__'
        depth = 1