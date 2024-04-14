from django.db import models
from django.contrib.auth import get_user_model
from Category.models import Category
from django.utils.crypto import get_random_string
import time
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from Comment.models import Comment
from Like_And_DisLike.models import Like_And_DisLike
from django.shortcuts import reverse


def upload_product_original_image(instance, filename):
    path = 'products/' + slugify(instance.title, allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name


class Product(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=50)
    slug = models.CharField(verbose_name='نامک', unique=True, max_length=50)
    short_text = models.TextField(verbose_name='توضیحات', max_length=250)
    text = models.TextField(verbose_name='متن')
    tags = models.CharField(verbose_name='تگ ها', max_length=250)
    price = models.IntegerField(verbose_name='قمیت')
    viewCount = models.IntegerField(verbose_name='تعداد بازدیدها', default=0)
    likeCount = models.IntegerField(verbose_name='تعداد لایک ها', default=0)
    commentCount = models.IntegerField(verbose_name='تعداد نظرات', default=0)
    status = models.BooleanField(verbose_name='وضعیت تایید', default=False)
    count = models.IntegerField(verbose_name='تعداد', default=1)
    is_removed = models.BooleanField(verbose_name='آیا حذف شده', default=False)

    suggestion_count = models.IntegerField(verbose_name='تعداد پیشنهاد خرید', default=0)
    original_image = models.ImageField(upload_to=upload_product_original_image, verbose_name='عکس', null=True)

    user = models.ForeignKey(verbose_name='فروشنده', to=get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='دسته بندی', to=Category, on_delete=models.CASCADE)

    colors = models.ManyToManyField(to='Color', related_query_name='product', verbose_name='رنگ ها')
    sizes = models.ManyToManyField(to='Size', related_query_name='product', verbose_name='سایز ها')

    comments = GenericRelation(Comment, related_query_name='products')
    likes_and_dislikes = GenericRelation(Like_And_DisLike, related_query_name='products')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    def __str__(self):
        return self.title


class NotifyUser(models.Model):
    user = models.ForeignKey(verbose_name='کاربر', to=get_user_model(), related_name='notifies',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name='محصول', to=Product, related_name='notifies', on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name='وضعیت فعال', default=True)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'اطلاع رسانی'
        verbose_name_plural = 'اطلاع رسانی ها'

    def __str__(self):
        return self.user.username + '-' + self.product.title


class Color(models.Model):
    name = models.CharField(verbose_name='نام', max_length=50)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.name


class Size(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=50)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'

    def __str__(self):
        return self.title


###############################################################

def upload_product_images(instance, filename):
    path = 'products/' + slugify(instance.product.title, allow_unicode=True) + '/images/'
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name


class Image(models.Model):
    image = models.ImageField(upload_to=upload_product_images, verbose_name='عکس', null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'عکس'
        verbose_name_plural = 'عکس ها'

    def __str__(self):
        return self.product.title



class Suggest(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='suggests', verbose_name='کاربر')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='suggests', verbose_name='محصول')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'پیشنهاد شده'
        verbose_name_plural = 'پیشنهاد شده ها'

    def __str__(self):
        return self.product.title + '-' + self.user.username
