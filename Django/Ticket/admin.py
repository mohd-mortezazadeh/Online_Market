from django.contrib import admin
from .models import *

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title' , 'status' , 'user']


@admin.register(TicketQuestion)
class QuestionTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket' , 'ShowText']

    def ShowText(self , obj):
        return obj.text[:50] + ' ...'

    ShowText.short_description = 'متن سوال'

@admin.register(TicketAnswer)
class AnswerTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket' , 'question' , 'ShowText']

    def ShowText(self , obj):
        return obj.text[:50] + ' ...'

    ShowText.short_description = 'متن پاسخ'