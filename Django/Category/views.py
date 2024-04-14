from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView , ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from .models import *
from .serializer import *

class CategoryViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CustomPagination
    search_fields = ['name']


class CategoryNullParentView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent__isnull=False)


class ParentListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    def get(self , request , self_id=0):
        if self_id == 0:
            categories = list(Category.objects.all().values())
        else:
            categories = list(Category.objects.exclude(pk=self_id).values())

        return Response(categories , 200)


class ParentView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    serializer_class = ParentSerializer
    queryset = Category.objects.all()