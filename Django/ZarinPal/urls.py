from django.urls import path
from .views import *

urlpatterns = [
    path('request/', pay , name='request-payment'),
    path('verify/', verify , name='verify'),
]
