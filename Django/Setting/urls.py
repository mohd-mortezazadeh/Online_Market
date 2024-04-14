from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('' , SettingsViewSet)

urlpatterns = [
    path('' , include(router.urls)),
]
