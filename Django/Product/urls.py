from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('accepted' , ProductAcceptedViewsSet)
router.register('rejected' , ProductRejectedViewsSet)
router.register('notify_users/active' , ActiveNotifyUsersViewsSet)
router.register('notify_users/inactive' , InActiveNotifyUsersViewsSet)
router.register('images' , ImagesViewSet)
router.register('colors' , ColorsViewSet)
router.register('sizes' , SizesViewSet)
router.register('suggests' , SuggestsViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('WithOutPagination/' , ProductAllList.as_view()),
    path('images/create/multiple/' , ProductImagesView.as_view()),
    path('users/list/' , UsersListView.as_view()),
    path('change/accepted' , ProductChangeAccepted.as_view()),
    path('notify_users/change/active/', NotifyUserChangeActive.as_view()),

    path('colors/all/WithOutPagination/' , ColorListWithOutPaginationView.as_view()),
    path('sizes/all/WithOutPagination/', SizeListWithOutPaginationView.as_view()),
]
