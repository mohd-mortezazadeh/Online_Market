from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from .models import *
from .serializer import *
from django.utils.translation import gettext_lazy as _

class ActiveSlidersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Slider.objects.filter(status=True)
    serializer_class = SliderSerializer
    pagination_class = CustomPagination
    search_fields = [
        'title',
        'image',
        'url',
        'priority'
    ]


class InActiveSlidersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Slider.objects.filter(status=False)
    serializer_class = SliderSerializer
    pagination_class = CustomPagination
    search_fields = [
        'title',
        'image',
        'url',
        'priority'
    ]


class ChangeSliderStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'active':
            pk = self.request.POST.get('id')
            slider = Slider.objects.get(pk=pk)
            slider.status = True
            slider.save()

            return Response( {'detail' : _('slider status has been set TRUE')}, 200)
        else:
            pk = self.request.POST.get('id')
            slider = Slider.objects.get(pk=pk)
            slider.status = False
            slider.save()

            return Response({'detail' : _('slider status has been set FALSE')}, 200)