from django.db import models
from django.contrib.auth import get_user_model
from Product.models import Product, Color, Size


class Cart(models.Model):
    user = models.ForeignKey(to=get_user_model() , related_name='carts' , on_delete=models.CASCADE , verbose_name='کاربر')
    product = models.ForeignKey(to=Product , on_delete=models.CASCADE , verbose_name='محصول')
    color = models.ForeignKey(to=Color , on_delete=models.CASCADE , verbose_name='رنگ' , null=True)
    size = models.ForeignKey(to=Size , on_delete=models.CASCADE , verbose_name='سایز' , null=True)

    count = models.IntegerField(verbose_name='تعداد' , default=1)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'


    def __str__(self):
        return self.user.username