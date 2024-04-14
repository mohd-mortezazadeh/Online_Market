from re import sub
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import permissions

class IsAdminMixin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = sub('Bearer ', '', request.META.get('HTTP_AUTHORIZATION', None))
            user_id = AccessToken(token).payload['user_id']
            user = User.objects.get(pk=user_id)
        except:
            user = request.user

        if user.is_authenticated and not user.is_superuser:
            return False

        return True


class IsAdminOrAuthorMixin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = sub('Bearer ', '', request.META.get('HTTP_AUTHORIZATION', None))
            user_id = AccessToken(token).payload['user_id']
            user = User.objects.get(pk=user_id)
        except:
            user = request.user

        if user.is_superuser or user.role_user_set.filter(role__title='author'):
            return True

        return False



class IsAdminOrShopManagerMixin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = sub('Bearer ', '', request.META.get('HTTP_AUTHORIZATION', None))
            user_id = AccessToken(token).payload['user_id']
            user = User.objects.get(pk=user_id)
        except:
            user = request.user

        if user.is_superuser or user.role_user_set.filter(role__title='manager'):
            return True

        return False