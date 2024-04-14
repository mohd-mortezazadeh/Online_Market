from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class ParentSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

class CategorySerializer(ModelSerializer):
    # parent = serializers.HyperlinkedRelatedField(
    #     view_name='parent-detail',
    #     lookup_field='pk',
    #     queryset=Category.objects.all(),
    #     required=False,
    #     allow_null=True
    # )
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all() , required=False , allow_null=True)
    class Meta:
        model = Category
        fields = '__all__'