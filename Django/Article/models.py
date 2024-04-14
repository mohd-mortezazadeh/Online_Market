from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from Category.models import Category
import time
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from Comment.models import Comment
from Like_And_DisLike.models import Like_And_DisLike


def upload_image(instance , filename):
    path = 'articles/' + slugify(instance.title , allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name

class Article(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=50)
    slug = models.CharField(verbose_name='اسلاگ (نامک)', unique=True , max_length=50)
    description = models.CharField(verbose_name='توضیحات' , max_length=250)
    body = models.TextField(verbose_name='متن')
    image = models.ImageField(verbose_name='عکس' , upload_to=upload_image , null=True)
    tags = models.CharField(verbose_name='تگ ها' , max_length=250)
    keywords = models.CharField(verbose_name='کلمات کلیدی' , max_length=250)
    status = models.IntegerField(verbose_name='وضعیت' , default=0)
    likeCount = models.IntegerField(verbose_name='تعداد لایک ها' , default=0)
    viewCount = models.IntegerField(verbose_name='تعداد بازدید ها' , default=0)
    commentCount = models.IntegerField(verbose_name='تعداد نظرات' , default=0)

    author = models.ForeignKey(verbose_name='نویسنده' , related_name='author_id' , to=get_user_model() , on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='دسته بندی' , related_name='category_id' , to=Category , on_delete=models.CASCADE)

    comments = GenericRelation(Comment, related_query_name='articles')
    likes_and_dislikes = GenericRelation(Like_And_DisLike , related_query_name='articles')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title