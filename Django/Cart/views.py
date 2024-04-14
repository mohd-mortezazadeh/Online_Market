from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from .models import *
from .serializer import *

class CartsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = CustomPagination
    search_fields = ['user__username' , 'product__title']