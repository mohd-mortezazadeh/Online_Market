from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from django.utils.translation import gettext_lazy as _
from .models import *
from .serializer import *

class LikesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Like_And_DisLike.objects.filter(type='like')
    serializer_class = Like_And_DisLike_Serializer
    pagination_class = CustomPagination
    search_fields = ['user__username']


class DisLikesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Like_And_DisLike.objects.filter(type='dislike')
    serializer_class = Like_And_DisLike_Serializer
    pagination_class = CustomPagination
    search_fields = ['user__username']


class ChangeType(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'like':
            pk = self.request.POST.get('id')
            like_and_dislike = Like_And_DisLike.objects.get(pk=pk)
            like_and_dislike.type = 'like'
            like_and_dislike.save()

            return Response({'detail': _('like_and_dislike type has been set LIKE')}, 200)
        else:
            pk = self.request.POST.get('id')
            like_and_dislike = Like_And_DisLike.objects.get(pk=pk)
            like_and_dislike.type = 'dislike'
            like_and_dislike.save()

            return Response({'detail': _('like_and_dislike type has been set DISLIKE')}, 200)
