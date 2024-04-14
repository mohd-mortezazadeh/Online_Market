from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from .models import User
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "username",
            "email",
            "first_name",
            "last_name",
            "phoneNumber",
            "is_superuser",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
            "image",
        ]

        read_only_fields = [
            "date_joined",
            "last_login",
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data.keys():
            password = validated_data.pop('password')
            user.set_password(password)

        user.save()
        return user