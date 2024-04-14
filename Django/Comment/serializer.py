from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Article.models import Article
from Article.serializer import ArticleSerializer
from Product.models import Product
from Product.serializer import ProductSerializer
from .models import *

class CommentedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Product):
            serializer = ProductSerializer(value)
        elif isinstance(value, Article):
            serializer = ArticleSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data

class CommentSerializer(ModelSerializer):
    content_object = CommentedObjectRelatedField(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=Comment.objects.filter(status=True , parent_id=None), write_only=True,
        required=False
    )

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1