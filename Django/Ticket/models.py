from django.db import models
from django.contrib.auth import get_user_model

class Ticket(models.Model):
    title = models.CharField(verbose_name='عنوان' , max_length=50)
    status = models.BooleanField(verbose_name='وضعیت' , default=True)
    user = models.ForeignKey(to=get_user_model() , on_delete=models.CASCADE , verbose_name='کاربر')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    ## You can create 'Ticket Questions' like this too:
         # ticket = models.ManyToManyField(to='TicketQuestion' , related_name='question_id')

    ## You can create 'Ticket Answers' like this too:
    # ticket = models.ManyToManyField(to='TicketQuestion' , related_name='question_id')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


    def __str__(self):
        return self.title



class TicketQuestion(models.Model):
    text = models.TextField(verbose_name='متن سوال')
    ticket = models.ForeignKey(to=Ticket , on_delete=models.CASCADE , verbose_name='تیکت')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'سوال های تیکت'
        verbose_name_plural = 'سوال های تیکت'

    def __str__(self):
        return self.text[:50] + ' ...'


class TicketAnswer(models.Model):
    text = models.TextField(verbose_name='متن پاسخ')
    ticket = models.ForeignKey(to=Ticket , on_delete=models.CASCADE , verbose_name='تیکت')
    question = models.ForeignKey(to=TicketQuestion , on_delete=models.CASCADE , verbose_name='سوال')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت' , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش' , auto_now=True)

    class Meta:
        verbose_name = 'پاسخ تیکت'
        verbose_name_plural = 'پاسخ های تیکت'

    def __str__(self):
        return self.text[:50] + ' ...'