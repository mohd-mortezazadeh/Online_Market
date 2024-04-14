from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Like_And_DisLike(models.Model):
    user = models.ForeignKey(to=User , related_name='likes_and_dislikes' , on_delete=models.CASCADE , verbose_name='کاربر')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE , verbose_name='مدل لایک-دیسلایک')
    object_id = models.PositiveIntegerField(verbose_name='شناسه مدل لایک-دیسلایک')
    content_object = GenericForeignKey()

    types_options = (('like', 'لایک'), ('dislike', 'دیسلایک'))
    type = models.CharField(max_length=10 , choices=types_options , verbose_name='نوع')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'لایک و دیسلایک'
        verbose_name_plural = 'لایک و دیسلایک ها'


    def __str__(self):
        return self.user.username
