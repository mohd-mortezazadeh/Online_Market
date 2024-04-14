from rest_framework.serializers import ModelSerializer
from .models import *

class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'