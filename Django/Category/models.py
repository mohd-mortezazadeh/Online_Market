from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name='نام' , max_length=50)
    slug = models.CharField(verbose_name='اسلاگ (نامک)' , unique=True , max_length=50)
    parent = models.ForeignKey(verbose_name='والد' , to='Category' , related_name='childs' , on_delete=models.CASCADE , null=True , blank=True)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name