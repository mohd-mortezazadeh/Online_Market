from django.contrib import admin
from .models import *

@admin.register(Like_And_DisLike)
class Like_And_DisLike_Admin(admin.ModelAdmin):
    list_display = ['user' , 'content_type' , 'type' , 'created_at' , 'updated_at']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]