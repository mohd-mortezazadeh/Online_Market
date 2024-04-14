from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from Product.models import Product, Color, Size
from Payment.models import Payment


class Order(models.Model):
    user = models.ForeignKey(verbose_name='کاربر', to=get_user_model() , related_name='orders' , on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name='محصول', to=Product , related_name='orders' , on_delete=models.CASCADE)
    payment = models.ForeignKey(verbose_name='پرداخت', to=Payment, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(to=Color, on_delete=models.CASCADE, verbose_name='رنگ')
    size = models.ForeignKey(to=Size, on_delete=models.CASCADE, verbose_name='سایز')

    count = models.IntegerField(verbose_name='تعداد', default=1)

    name = models.CharField(verbose_name='نام', max_length=50)
    family = models.CharField(verbose_name='نام خانوادگی', max_length=50)
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(verbose_name='موبایل' , max_length=11)
    address1 = models.TextField(verbose_name='آدرس 1')
    address2 = models.TextField(verbose_name='آدرس 2', null=True, blank=True)
    post_code = models.CharField(verbose_name='کد پستی' , max_length=10, validators=[RegexValidator(r"^\d{10}$")])

    PAYMENTS_OPTIONS = (
        ('online', 'آنلاین'),
        ('cash', 'نقدی')
    )

    STATUS_OPTIONS = (
        ('sending', 'درحال ارسال'),
        ('posted', 'ارسال شده'),
        ('delivered', 'تحویل داده شده')
    )

    payment_type = models.CharField(verbose_name='نوع پرداخت', max_length=6, choices=PAYMENTS_OPTIONS, null=True,
                                    blank=True)
    status = models.CharField(verbose_name='وضعیت ارسال', max_length=9, choices=STATUS_OPTIONS, default='sending',
                              null=True, blank=True)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return self.user.username + '-' + self.product.title
