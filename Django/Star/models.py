from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from Product.models import Product

User = get_user_model()

class Star(models.Model):
    score = models.IntegerField(verbose_name='امتیاز' , default=0 , validators=[MinValueValidator(0), MaxValueValidator(5)])

    user = models.ForeignKey(to=User , on_delete=models.CASCADE , related_name='stars' , verbose_name='کاربر')
    product = models.ForeignKey(to=Product , on_delete=models.CASCADE , related_name='stars' , verbose_name='محصول')


    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)


    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'


    def __str__(self):
        return self.user.username + '-' + self.product.title