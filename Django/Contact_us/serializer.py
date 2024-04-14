from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = Contact_us
        fields = '__all__'