from rest_framework import serializers
from Comment.models import Comment
from Product.models import Product
from Article.models import Article


class CommentSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=50)
    text = serializers.CharField(required=True)
    object_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)
    parent_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        title, text, object_id, user_id, type = validated_data['title'], validated_data['text'], \
                                                           validated_data['object_id'] \
            , validated_data['user_id'], validated_data['type']

        if type == 'product':
            object = Product.objects.get(pk=object_id)
        else:
            object = Article.objects.get(pk=object_id)

        if 'parent_id' in validated_data:
            parent_id = validated_data['parent_id']
        else:
            parent_id = None

        comment = Comment.objects.create(title=title, text=text, content_object=object, user_id=user_id , parent_id=parent_id)
        return comment
