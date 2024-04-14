from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('' , UsersViewSet)
router.register('blocks/list' , BlockUsersViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('all/WithOutPagination/' , UsersListWithoutPagination.as_view()),
    path('change/block_status/' , ChangeBlockStatus.as_view())
]
