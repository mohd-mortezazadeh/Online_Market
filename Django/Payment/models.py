from django.db import models
from Product.models import Product , Color , Size
from django.contrib.auth import get_user_model
from Coupon.models import Coupon

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(to=get_user_model() , on_delete=models.CASCADE , verbose_name='کاربری')
    amount = models.CharField(verbose_name='مبلغ' , max_length=255 , null=True)
    coupon = models.ForeignKey(to=Coupon , on_delete=models.CASCADE , verbose_name='کد تخفیف' , null=True)

    status = models.BooleanField(verbose_name='وضعیت' , default=False)

    authority = models.CharField(verbose_name='کد بازگشتی درگاه' , max_length=255 , null=True)
    ref_code = models.CharField(verbose_name='شناسه پیگیری' , max_length=255 , null=True)

    created_at = models.DateTimeField(verbose_name='تاریخ خرید' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'


    def __str__(self):
        return self.user.username + f"( {self.ref_code} )"