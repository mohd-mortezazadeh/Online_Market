from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from django.utils.translation import gettext_lazy as _
from .models import *
from .serializer import *


class SuccessOrdersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Order.objects.filter(status='delivered')
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    search_fields = [
        'user__username',
        'product__title',
        'product__price',
        'color__name',
        'size__title',
        'count',
        'payment__ref_code',
        'name',
        'family',
        'email',
        'address1',
        'address2',
        'post_code',
    ]


class UnSuccessOrdersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Order.objects.exclude(status='delivered')
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    search_fields = [
        'user__username',
        'product__title',
        'product__price',
        'color__name',
        'size__title',
        'count',
        'payment__ref_code',
        'name',
        'family',
        'email',
        'address1',
        'address2',
        'post_code',
    ]

############################################################

class ChangeOrderPayment(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self, request):
        pk = self.request.POST.get('id')
        order = Order.objects.get(pk=pk)
        if self.request.POST.get('type') == 'success':
            order.status = 'delivered'
            order.save()
            return Response({'detail': _('order status has been set TRUE')}, 200)
        else:
            order.status = 'posted'
            order.save()
            return Response({'detail': _('order status has been set FALSE')}, 200)
