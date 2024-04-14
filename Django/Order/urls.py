from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('successful' , SuccessOrdersViewSet)
router.register('unsuccessful' , UnSuccessOrdersViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('change/status/' , ChangeOrderPayment.as_view())
]
