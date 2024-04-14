from django.urls import path
from .views import *

urlpatterns = [
    path('orders/success/' , SuccessOrdersViewSet.as_view()),
    path('orders/fail/', FailOrdersViewSet.as_view()),
]
