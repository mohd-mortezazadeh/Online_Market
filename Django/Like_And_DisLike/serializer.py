from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Article.models import Article
from Article.serializer import ArticleSerializer
from Product.models import Product
from Product.serializer import ProductSerializer
from .models import *

class Like_And_DisLiked_ObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Product):
            serializer = ProductSerializer(value)
        elif isinstance(value, Article):
            serializer = ArticleSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data

class Like_And_DisLike_Serializer(ModelSerializer):
    content_object = Like_And_DisLiked_ObjectRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.filter(block_status=False), write_only=True
    )

    class Meta:
        model = Like_And_DisLike
        fields = '__all__'
        depth = 1