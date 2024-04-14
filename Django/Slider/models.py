from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
import time


def upload_image(instance , filename):
    path = 'sliders/' + slugify(instance.title , allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name

class Slider(models.Model):
    title = models.CharField(verbose_name='عنوان' , max_length=50 , null=True)
    image = models.ImageField(upload_to=upload_image , verbose_name='عکس')
    url = models.URLField(verbose_name='آدرس')
    priority = models.IntegerField(verbose_name='الویت')
    status = models.BooleanField(default=True , verbose_name='وضعیت')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'


    def __str__(self):
        return self.title