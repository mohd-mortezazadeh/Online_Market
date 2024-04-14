from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class PaymentSerializer(ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Payment
        fields = '__all__'
        depth = 1