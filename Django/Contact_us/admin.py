from django.contrib import admin
from .models import *

@admin.register(Contact_us)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name' , 'email' , 'website' , 'show_text']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    def show_text(self , obj):
        return obj.text[:50] + '...'

    show_text.short_description = 'متن'