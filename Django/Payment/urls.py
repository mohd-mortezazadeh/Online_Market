from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('successful' , SuccessfulPaymentsViewSet)
router.register('unsuccessful' , UnSuccessfulPaymentsViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('change/status/' , ChangePaymentStatus.as_view())
]


