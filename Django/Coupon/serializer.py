from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'