from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Comment(models.Model):
    title = models.CharField(verbose_name='عنوان' , max_length=50)
    text = models.TextField(verbose_name='متن')
    status = models.BooleanField(default=False , verbose_name='وضعیت')

    user = models.ForeignKey(to=User , on_delete=models.CASCADE , related_name='comments' , verbose_name='کاربر')
    parent = models.OneToOneField(to='Comment' , on_delete=models.CASCADE , related_name='answer' , verbose_name='والد' , null=True , blank=True)

    content_type = models.ForeignKey(ContentType, related_name='comments' , on_delete=models.CASCADE , verbose_name='مدل نظر')
    object_id = models.PositiveIntegerField(verbose_name='شناسه مدل نظر')
    content_object = GenericForeignKey()

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


    def __str__(self):
        return self.title