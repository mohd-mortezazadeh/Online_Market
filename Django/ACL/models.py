from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Role(models.Model):
    title = models.CharField(verbose_name='عنوان' , max_length=50)
    label = models.CharField(verbose_name='برچسب' , max_length=50)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'نقش'
        verbose_name_plural = 'نقش ها'


    def __str__(self):
        return self.title


class Permission(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=50)
    label = models.CharField(verbose_name='برچسب', max_length=50)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'دسترسی'
        verbose_name_plural = 'دسترسی ها'

    def __str__(self):
        return self.title


######################################################################################

class Role_User(models.Model):
    role = models.ForeignKey(to=Role , on_delete=models.CASCADE , verbose_name='نقش ')
    user = models.ForeignKey(to=get_user_model() , on_delete=models.CASCADE , verbose_name='کاربر')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'نقش-کاربری'
        verbose_name_plural = 'نفش-کاربری ها'


    def __str__(self):
        return self.role.title + ' - ' + self.user.username



class Role_Permission(models.Model):
    role = models.ForeignKey(to=Role , on_delete=models.CASCADE , verbose_name='نقش')
    permission = models.ForeignKey(to=Permission , on_delete=models.CASCADE , verbose_name='دسترسی')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'نقش-دسترسی'
        verbose_name_plural = 'نقش-دسترسی ها'

    def __str__(self):
        return self.role.title + ' - ' + self.permission.title