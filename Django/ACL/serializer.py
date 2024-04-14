from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class Role_UserSerializer(ModelSerializer):
    class Meta:
        model = Role_User
        fields = '__all__'
        depth = 1


class Role_PermissionSerializer(ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )
    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), source='permission', write_only=True
    )

    class Meta:
        model = Role_Permission
        fields = '__all__'
        depth = 1