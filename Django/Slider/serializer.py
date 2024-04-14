from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *


class SliderSerializer(ModelSerializer):
    image = serializers.ImageField(required=False, use_url=True)
    class Meta:
        model = Slider
        fields = '__all__'