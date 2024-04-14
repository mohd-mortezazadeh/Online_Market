from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from Order.models import Order
from Order.serializer import OrderSerializer
from config.pagination import CustomPagination


class SuccessOrdersViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    # search_fields = ['user__username' , 'product__title']

    def get_queryset(self):
        return Order.objects.filter(status=True , user=self.request.user)


class FailOrdersViewSet(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    # search_fields = ['user__username' , 'product__title']

    def get_queryset(self):
        return Order.objects.filter(status=False , user=self.request.user)