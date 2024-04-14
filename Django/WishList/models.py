from django.db import models
from django.contrib.auth import get_user_model
from Product.models import Product

User = get_user_model()

class Wishlist(models.Model):
    user = models.ForeignKey(to=User , on_delete=models.CASCADE , verbose_name='کاربر')
    product = models.ForeignKey(to=Product , on_delete=models.CASCADE , verbose_name='محصول')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)


    class Meta:
        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'


    def __str__(self):
        return self.user.username + '-' + self.product.title