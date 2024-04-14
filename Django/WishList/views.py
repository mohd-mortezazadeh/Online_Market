from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from .models import *
from .serializer import *

class WishlistsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    pagination_class = CustomPagination
    search_fields = ['user__username' , 'product__title']