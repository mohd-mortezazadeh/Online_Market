from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from .models import *
from .serializer import *
from config.pagination import CustomPagination


class SettingsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    pagination_class = CustomPagination
    search_fields = ['key' , 'value']