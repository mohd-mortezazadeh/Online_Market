from django.contrib import admin
from .models import *

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['title' , 'text' , 'status' , 'user' , 'parent' , 'content_type']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]