from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view() , name='login'),
    path('register/', Register.as_view() , name='register'),
    path('logout/', Logout.as_view() , name='logout'),
    path('isLogin/', CheckLogin.as_view()),
    path('profile/' , Profile.as_view()),
    path('profile/update/', ProfileUpdate.as_view()),

    path('password/change/<int:pk>/', ChangePasswordView.as_view()),
    path('password/reset/', SendEmailView.as_view()),
    path('password/reset/confirm/', ResetPasswordView.as_view()),
    path('email/verification/', VerifyEmailView.as_view(), name="verify-email"),
    path('email/verification/check/', CheckEmailVerification.as_view()),
]
