from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('roles' , RolesViewSet)
router.register('permissions' , PermissionsViewSet)
router.register('role_user' , Role_UsersViewSet)
router.register('role_permission' , Role_PermissionViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('role_user/create/update/' , Role_UsersCreateUpdateMultipleViewSet.as_view()),
    path('role_permission/create/update/' , Role_PermissionsCreateUpdateMultipleViewSet.as_view()),

    path('check/roles/' , CheckRolesViewSet.as_view()),

    path('roles/all/WithOutPagination/' , RolesWithOutPaginationViewSet.as_view()),
    path('permissions/all/WithOutPagination/', PermissionWithOutPaginationViewSet.as_view()),
]
