from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from .models import *
from .serializer import *
from config.pagination import CustomPagination

class StarsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    pagination_class = CustomPagination
    search_fields = ['score','user__username','product__title']