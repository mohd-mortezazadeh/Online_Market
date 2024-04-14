from django.contrib.sites.shortcuts import get_current_site
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.generics import GenericAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from ACL.models import Role_User
from User.serializers import UserSerializer
from .serializers import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ACL.serializer import Role_UserSerializer


def GetAuthUser(request):
    user = model_to_dict(request.user)
    if request.user.image_url is not None:
        user['image'] = user['image'].url
    else:
        user['image'] = None

    roles = Role_UserSerializer(request.user.role_user_set.all(), many=True)
    user['roles'] = roles.data

    return user


def AuthenticateUser(username, password, self):
    user = authenticate(self.request, username=username, password=password)
    if user is not None:
        tokens = get_tokens_for_user(user)
        login(self.request, user)

        data = {
            "access": tokens['access'],
            "refresh": tokens['refresh'],
            "user": GetAuthUser(self.request)
        }

        return data

    return False


#############################################################################################
class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=self.request.POST)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            data = AuthenticateUser(username, password, self)
            if data:
                if not data['user']['block_status']:
                    return JsonResponse(data, safe=False, status=200)
                else:
                    return JsonResponse({'message': 'شما توسط مدیر سایت مسدود شده اید!'}, safe=False, status=401)

        return JsonResponse({'message': 'نام کاربری و یا رمز عبور اشتباه است!'}, safe=False, status=401)


class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                data = AuthenticateUser(username, password, self)
                if data:
                    current_site = get_current_site(request).domain
                    relativeLink = reverse('verify-email')
                    link = 'http://' + current_site + relativeLink

                    msg = EmailMultiAlternatives('تایید حساب کاربری', 'This is test.', 'ashkan@gmail.com',
                                                 [data['user']['email']])
                    html_content = get_template('verify_email.html').render(
                        {'link': link, 'token': data['access'], 'username': username})
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    return Response(data, status=200)

        return Response({'message': 'username/password is not correct!'}, 401)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        if 'type' in request.POST and request.POST['type'] == 'fronted':
            return redirect('/')
        else:
            return Response({'status': True}, 200)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class CheckLogin(APIView):
    def post(self, request):
        data = {
            'login_status': self.request.user.is_authenticated,
            'super_user_status': self.request.user.is_superuser,
        }
        if data['login_status']:
            data['user'] = GetAuthUser(self.request)
        return Response(data, 200)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'user': GetAuthUser(request)
        }
        return Response(data, status=200)


class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        user = get_object_or_404(get_user_model() , pk=user_id)

        serializer = UserSerializer(instance=user , data=request.data , partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({'detail' : 'user updated successfully'}, status=200)


class CheckEmailVerification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            'verified_at': self.request.user.email_verified_at,
        }
        return Response(data, 200)


##############################################
## Create Tokens ##
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


##############################################################################
## Reset Password ##
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from .utils import *


class SendEmailView(GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        serializer = SendEmailSerializer(data=self.request.POST)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.validated_data['email'])

            if CheckLinkExpire(user.id):
                return Response({'detail': [
                    'email has been sent, check your received email and you you can get New Link after 15 minutes done']},
                    404)

            new_token = CreateToken()
            ip = self.request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[
                0].strip()

            ResetPassword.objects.create(token=new_token, user_id=user.id,
                                         user_agent=self.request.META['HTTP_USER_AGENT'], ip=ip)

            msg = EmailMultiAlternatives('بازیابی رمز عبور', 'This is test.', 'from@example.com', ['to@example.com'])
            html_content = get_template('reset_password.html').render({'token': new_token, 'username': user.username})
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({'detail': 'Email has been successfully sent , check your received emails'}, 200)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=self.request.POST)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            password = serializer.validated_data['new_password']

            reset_password_obj = ResetPassword.objects.get(token=token)
            user = reset_password_obj.user

            if not CheckLinkExpire(user.id):
                return Response({'detail': ['this token has been expired']}, 404)

            user.set_password(password)
            reset_password_obj.is_used = True

            reset_password_obj.save()
            user.save()

        return Response({'detail': 'Your password has been successfully changed'})


##############################################################################################
## Verify Email ##
from rest_framework_simplejwt.tokens import AccessToken


class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        token = request.POST.get('token')
        try:
            user_id = AccessToken(token).payload['user_id']
            user = User.objects.get(pk=user_id)
            user.email_verified_at = datetime.today()
            user.is_active = True
            user.save()

            return Response({'detail': 'Your Account has been verified successfully'})
        except:
            return Response({'error': ['Token is invalid or Expired']}, 400)
