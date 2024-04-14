from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from Permission.admin import IsAdminMixin
from .serializers import *
from config.pagination import CustomPagination
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UsersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = User.objects.filter(block_status=False)
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phoneNumber',
    ]


class BlockUsersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = User.objects.filter(block_status=True)
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phoneNumber',
    ]


class UsersListWithoutPagination(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = User.objects.filter(block_status=False)
    serializer_class = UserSerializer

#################################################
class ChangeBlockStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self , request):
        pk = self.request.POST.get('id')

        if self.request.POST.get('type') == 'block':
            user = User.objects.get(pk=pk)
            user.block_status = True
            user.save()

            return Response( {'detail' : _('user block status has been set TRUE')}, 200)
        else:
            user = User.objects.get(pk=pk)
            user.block_status = False
            user.save()

            return Response({'detail' : _('user block status has been set FALSE')}, 200)