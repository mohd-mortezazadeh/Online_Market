from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('likes' , LikesViewSet)
router.register('dislikes' , DisLikesViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('change/type/' , ChangeType.as_view())
]
