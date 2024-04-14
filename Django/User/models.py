from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import time
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from .managers import UserManager

def upload_image(instance , filename):
    path = 'users/' + slugify(instance.username , allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name


class User(AbstractBaseUser ,  PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phoneNumber = models.CharField(_('phone number'), max_length=11, blank=True)
    email_verified_at = models.DateTimeField(verbose_name=_('email_verified_at') , null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    level = models.CharField(_('level') , default='user' , max_length=50)
    block_status = models.BooleanField(_('block_status') , default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email' , 'password']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


    @property
    def image_url(self):
        """
        Return self.photo.url if self.photo is not None,
        'url' exist and has a value, else, return None.
        """
        if self.image:
            return getattr(self.image, 'url', None)
        return None

    def get_username(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)