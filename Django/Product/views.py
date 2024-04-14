from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from Permission.admin import IsAdminOrShopManagerMixin
from config.pagination import CustomPagination

from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from User.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class ProductAcceptedViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Product.objects.filter(status=True).filter(is_removed=False)
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    search_fields = [
        'title',
        'slug',
        'short_text',
        'text',
        'price',
        'user__username'
    ]


class ProductRejectedViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Product.objects.filter(status=False).filter(is_removed=False)
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    search_fields = [
        'title',
        'slug',
        'short_text',
        'text',
        'price',
        'user__username'
    ]


class ActiveNotifyUsersViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = NotifyUser.objects.filter(active=True)
    serializer_class = NotifyUserSerializer
    pagination_class = CustomPagination
    search_fields = [
        'product__title',
        'product__slug',
        'user__username'
    ]


class InActiveNotifyUsersViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = NotifyUser.objects.filter(active=False)
    serializer_class = NotifyUserSerializer
    pagination_class = CustomPagination
    search_fields = [
        'product__title',
        'product__slug',
        'user__username'
    ]


class ProductAllList(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ImagesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    pagination_class = CustomPagination
    search_fields = ['product__title']



class ColorsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    pagination_class = CustomPagination
    search_fields = ['name']


class SizesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    pagination_class = CustomPagination
    search_fields = ['title']


class SuggestsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Suggest.objects.all()
    serializer_class = SuggestSerializer
    pagination_class = CustomPagination
    search_fields = ['product__title' , 'user__username']


class ProductChangeAccepted(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'accept':
            pk = self.request.POST.get('id')
            product = Product.objects.get(pk=pk)
            product.status = True
            product.save()

            return Response( {'detail' : _('product status has been set TRUE')}, 200)
        else:
            pk = self.request.POST.get('id')
            product = Product.objects.get(pk=pk)
            product.status = False
            product.save()

            return Response({'detail' : _('product status has been set FALSE')}, 200)


class NotifyUserChangeActive(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'active':
            pk = self.request.POST.get('id')
            notify_user = NotifyUser.objects.get(pk=pk)
            notify_user.active = True
            notify_user.save()

            return Response( {'detail' : _('notify_user active has been set TRUE')}, 200)
        else:
            pk = self.request.POST.get('id')
            notify_user = NotifyUser.objects.get(pk=pk)
            notify_user.active = False
            notify_user.save()

            return Response({'detail' : _('notify_user active has been set FALSE')}, 200)


class ProductImagesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]

    def post(self, request):
        product = Product.objects.get(pk=self.request.POST['product'])

        for item in self.request.FILES:
            Image.objects.create(product=product , image=self.request.FILES[item])

        return Response({'status' : 'OK'} , 200)

###########################################################################

class UsersListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ColorListWithOutPaginationView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeListWithOutPaginationView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ColorListByProductID(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]

    def get(self , request , pk):
        product = Product.objects.get(id=pk)
        colors = product.colors.all()
        serializer = ColorSerializer(colors , many=True)
        return Response(serializer.data , 200)


class SizeListByProductID(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]

    def get(self , request , pk):
        product = Product.objects.get(id=pk)
        sizes = product.sizes.all()
        serializer = SizeSerializer(sizes , many=True)
        return Response(serializer.data , 200)


class SizeListWithOutPagination(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrShopManagerMixin]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer