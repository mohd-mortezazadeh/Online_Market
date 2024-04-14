from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('active' , ActiveSlidersViewSet)
router.register('disable' , InActiveSlidersViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('change/status/' , ChangeSliderStatus.as_view())
]
