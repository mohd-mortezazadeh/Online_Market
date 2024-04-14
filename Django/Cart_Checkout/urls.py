from django.urls import path
from .views import *

urlpatterns = [
    ## Steps ##
    path('carts/' , CartsList.as_view() , name='carts-list'),
    path('fill_data/' , FillData.as_view() , name='fill-data'),
    path('payment/method/' , ChoosePaymentMethod.as_view() , name='payment-method'),
    path('verification/' , Verification.as_view() , name='orders-verification'),

    ## Operations ##
    path('carts/change/count/' , ChangeCartCount.as_view() , name='count-change'),
    path('carts/delete/', DeleteCart.as_view(), name='cart-delete'),
]