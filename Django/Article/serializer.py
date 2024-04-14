from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from Category.models import Category as Cat
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

class ArticleSerializer(ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.filter(parent__isnull=False))
    image  = serializers.ImageField(required=False , use_url=True)
    class Meta:
        model = Article
        fields = '__all__'