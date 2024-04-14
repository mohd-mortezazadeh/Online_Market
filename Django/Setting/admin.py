from django.contrib import admin
from .models import *

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key' , 'value' ,  'created_at', 'updated_at']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]