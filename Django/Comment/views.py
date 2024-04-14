from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from .models import *
from .serializer import *

class CommentsAcceptedViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Comment.objects.filter(status=True)
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'text', 'user__username']


class CommentsNotAcceptedViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Comment.objects.filter(status=False)
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'text', 'user__username']


class ChangeCommentStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'accept':
            pk = self.request.POST.get('id')
            comment = Comment.objects.get(pk=pk)
            comment.status = True
            comment.save()

            return Response({'detail': _('comment status has been set TRUE')}, 200)
        else:
            pk = self.request.POST.get('id')
            comment = Comment.objects.get(pk=pk)
            comment.status = False
            comment.save()

            return Response({'detail': _('comment status has been set FALSE')}, 200)