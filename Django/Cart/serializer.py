from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'