from django.db import models

class Contact_us(models.Model):
    name = models.CharField(verbose_name='نام' , max_length=50)
    email = models.EmailField(verbose_name='ایمیل')
    website = models.CharField(verbose_name='وبسایت' , max_length=50 , null=True , blank=True)
    text = models.TextField(verbose_name='متن')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس با ما ها'

    def __str__(self):
        return self.name