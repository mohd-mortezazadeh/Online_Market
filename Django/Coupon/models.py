from django.db import models
from django.contrib.auth import get_user_model

class Coupon(models.Model):
    code = models.CharField(verbose_name='کد' , max_length=250)
    percent = models.IntegerField(verbose_name='درصد تخفیف')
    uses_number = models.IntegerField(verbose_name='تعداد قابل استفاده' , default=1)
    expiration = models.CharField(max_length=50 , verbose_name='تاریخ انقضا')

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE , verbose_name='کاربر' , null=True , blank=True)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف ها'


    def __str__(self):
        return self.code