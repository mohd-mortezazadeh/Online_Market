from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from .serializer import *
from .models import *

class ContactsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Contact_us.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = CustomPagination
    search_fields = ['name', 'email', 'website' , 'text']