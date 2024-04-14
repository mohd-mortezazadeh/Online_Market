from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from rest_framework.exceptions import ValidationError
from .models import *
from .serializer import *


class RolesViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'label']


class PermissionsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'label']


class Role_UsersViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Role_User.objects.all()
    serializer_class = Role_UserSerializer
    pagination_class = CustomPagination
    search_fields = ['role__title' , 'role__label' , 'user__username' , 'user__email' ]


class Role_PermissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Role_Permission.objects.all()
    serializer_class = Role_PermissionSerializer
    pagination_class = CustomPagination
    search_fields = ['role__title', 'role__label', 'permission__title', 'permission__label']


##############################################################################

class RolesWithOutPaginationViewSet(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PermissionWithOutPaginationViewSet(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

#######################################################

def SyncRolesToUser(self):
    if 'user' not in self.request.data or self.request.data['user'] is None:
        raise ValidationError({'user': ["This field may not be blank."], })

    if 'roles' not in self.request.data or self.request.data['roles'] == []:
        raise ValidationError({'roles': ["This field may not be blank."], })

    user_id = self.request.data['user']
    roles = self.request.data['roles']

    for item in roles:
        Role_User.objects.get_or_create(
            role_id=item,
            user_id=user_id,
            defaults={'role_id': item, 'user_id': user_id},
        )


class Role_UsersCreateUpdateMultipleViewSet(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    def post(self, request):
        SyncRolesToUser(self)
        return Response({'message': 'Roles has been sync to selected user'}, 200)

    def put(self, request):
        SyncRolesToUser(self)
        return Response({'message': 'Roles has been sync to selected user'}, 200)

##################################################################

def SyncPermissionsToRole(self):
    if 'role' not in self.request.data or self.request.data['role'] is None:
        raise ValidationError({'role': ["This field may not be blank."], })

    if 'permissions' not in self.request.data or self.request.data['permissions'] == []:
        raise ValidationError({'permissions': ["This field may not be blank."], })

    role_id = self.request.data['role']
    permissions = self.request.data['permissions']

    for item in permissions:
        Role_Permission.objects.get_or_create(
            role_id=role_id,
            permission_id=item,
            defaults={'permission_id': item, 'role_id': role_id},
        )


class Role_PermissionsCreateUpdateMultipleViewSet(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self, request):
        SyncPermissionsToRole(self)
        return Response({'message': 'Permission has been sync to selected role'}, 200)

    def put(self, request):
        SyncPermissionsToRole(self)
        return Response({'message': 'Permission has been sync to selected role'}, 200)


######################################################################################################

class CheckRolesViewSet(APIView):
    def post(self, request):
        roles = request.data.get('roles' , None)
        result = Role_User.objects.filter(role__title__in=roles , user=request.user)

        if len(result) == len(roles) or request.user.is_superuser:
            return Response({'status': True}, 200)

        return Response({'status': False}, 403)