from django.contrib import admin
from .models import *

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']