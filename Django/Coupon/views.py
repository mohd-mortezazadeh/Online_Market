from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from .models import *
from .serializer import *

class CouponsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    pagination_class = CustomPagination
    search_fields = ['code', 'percent', 'uses_number' , 'expiration' , 'user__username']
