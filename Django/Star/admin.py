from django.contrib import admin
from .models import *

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ['score' , 'product' , 'user' , 'created_at' , 'updated_at']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]