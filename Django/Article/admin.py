from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [ "title" ,"slug","description","status","likeCount","viewCount"
        ,"commentCount" , "image_tag" , "author" , "category" ,"created_at","updated_at" ]

    readonly_fields = ['likeCount' , 'viewCount' , 'commentCount']

    def image_tag(self, obj):
        return format_html('<img src="{}" width=50 />'.format(obj.image.url))

    image_tag.short_description = 'عکس'