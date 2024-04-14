from rest_framework.generics import RetrieveAPIView , ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminOrAuthorMixin
from .serializer import *
from config.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class ArticleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrAuthorMixin]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'description', 'body', 'author__username' , 'category__name']


class AuthorListView(ListAPIView):
    permission_classes = [IsAuthenticated , IsAdminOrAuthorMixin]
    queryset = User.objects.filter(role_user__role__title='author')
    serializer_class = AuthorSerializer


class AuthorView(RetrieveAPIView):
    queryset = User.objects.filter(role_user__role__title='author')
    serializer_class = AuthorSerializer