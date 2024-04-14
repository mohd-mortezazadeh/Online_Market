from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from django.utils.translation import gettext_lazy as _
from .models import *
from .serializer import *


class SuccessfulPaymentsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Payment.objects.filter(status=True)
    serializer_class = PaymentSerializer
    pagination_class = CustomPagination
    search_fields = [
        'user__username',
        'amount',
        'coupon__code',
        'ref_code',
    ]


class UnSuccessfulPaymentsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Payment.objects.filter(status=False)
    serializer_class = PaymentSerializer
    pagination_class = CustomPagination
    search_fields = [
        'user__username',
        'amount',
        'coupon__code',
        'ref_code',
    ]

############################################################

class ChangePaymentStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'success':
            pk = self.request.POST.get('id')
            payment = Payment.objects.get(pk=pk)
            payment.status = True
            payment.save()

            return Response( {'detail' : _('payment status has been set TRUE')}, 200)
        else:
            pk = self.request.POST.get('id')
            payment = Payment.objects.get(pk=pk)
            payment.status = False
            payment.save()

            return Response({'detail' : _('payment status has been set FALSE')}, 200)