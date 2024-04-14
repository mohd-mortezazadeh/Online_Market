from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ResetPassword(models.Model):
    token  = models.CharField(max_length=255 , unique=True , verbose_name='توکن')
    ip = models.GenericIPAddressField(verbose_name='آی پی')
    user_agent = models.CharField(max_length=265 , verbose_name='یوزر ایجنت')
    is_used = models.BooleanField(default=False , verbose_name='آیا استفاده شده است')

    user = models.ForeignKey(to=User , on_delete=models.CASCADE , verbose_name='کاربر')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)