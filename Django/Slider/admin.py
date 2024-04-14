from django.contrib import admin
from django.utils.html import format_html

from .models import *

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title' , 'image_tag' , 'url' , 'priority' , 'status' , 'created_at' , 'updated_at']
    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    def image_tag(self, obj):
        if obj.image:
            img = obj.image.url
            return format_html('<img src="{}" width=50 />'.format(img))

        return None

    image_tag.short_description = 'عکس'