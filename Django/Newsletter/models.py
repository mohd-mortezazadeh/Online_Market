from django.db import models

class Newsletter(models.Model):
    email = models.EmailField(verbose_name='ایمیل')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'خبرنامه'
        verbose_name_plural = 'خبرنامه'


    def __str__(self):
        return self.email