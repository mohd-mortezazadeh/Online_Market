from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class SettingSerializer(ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'