from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('accepted' , CommentsAcceptedViewSet)
router.register('NotAccepted' , CommentsNotAcceptedViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('change/status/' , ChangeCommentStatus.as_view()),
]
