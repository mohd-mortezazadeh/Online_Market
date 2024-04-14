from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [ "title" , "price" , "count" ,"likeCount","status" , "suggestion_count" ,"is_removed"
        ,"image_tag","user","category" , "ShowColors" , "ShowSizes" ,"created_at","updated_at" ]

    readonly_fields = ['created_at', 'updated_at' , 'likeCount' , 'viewCount' , 'commentCount']
    filter_horizontal = ('colors', 'sizes')

    def ShowColors(self , obj):
        return ' , '.join([item.name for item in obj.colors.all()])



    def ShowSizes(self, obj):
        return ' , '.join([item.title for item in obj.sizes.all()])



    def image_tag(self, obj):
        if obj.original_image:
            img = obj.original_image.url
            return format_html('<img src="{}" width=50 />'.format(img))

        return None


    image_tag.short_description = 'عکس اصلی'
    ShowColors.short_description = 'رنگ ها'
    ShowSizes.short_description = 'سایز ها'


@admin.register(NotifyUser)
class NotifyUserAdmin(admin.ModelAdmin):
    list_display = [ 'user' , 'product' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Image)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = [ "product" , "image" ]
    readonly_fields = ['created_at', 'updated_at']


    def image_tag(self, obj):
        if obj.image:
            img = obj.image.url
            return format_html('<img src="{}" width=50 />'.format(img))

        return None

    image_tag.short_description = 'عکس'



####################################################################################
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = [ 'name' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = [ 'title' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Suggest)
class SuggestAdmin(admin.ModelAdmin):
    list_display = [ 'product' , 'user' , 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']