from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from .models import *
from .serializer import *
from config.pagination import CustomPagination

class NewslettersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    pagination_class = CustomPagination
    search_fields = ['email']