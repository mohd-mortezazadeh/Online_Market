from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.utils.translation import ugettext_lazy as _
from .models import *

User = get_user_model()

class LoginSerializer(Serializer):
    username = serializers.CharField(max_length=50 , required=True)
    password = serializers.CharField(max_length=50 , required=True)


class RegisterSerializer(Serializer):
    username = serializers.CharField(max_length=50 , required=True ,  validators=[UniqueValidator(queryset=User.objects.all() , message=_('این نام کاربری قبلا انتخاب شده است'))])
    email = serializers.EmailField(max_length=50 , required=True , validators=[UniqueValidator(queryset=User.objects.all() , message=_('این ایمیل قبلا انتخاب شده است'))])
    password = serializers.CharField(max_length=50 , required=True)
    password2 = serializers.CharField(max_length=50, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": ["Password fields didn't match."]})

        return attrs

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user = User(username=username , email=email)
        user.set_password(password)
        user.save()

        return user



class ChangePasswordSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": ["Password fields didn't match."]})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(["Old password is not correct"])
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance



####################################################
## Reset Password ##

class SendEmailSerializer(Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError([_('There is no account with submitted email')])

        return value



class ResetPasswordSerializer(Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_token(self, value):
        if not ResetPassword.objects.filter(token=value).exists():
            raise serializers.ValidationError([_('This token is expired or is not for you')])

        return value


###############################################################################################

class VerifyEmailSerializer(Serializer):
    email = serializers.EmailField(required=True)