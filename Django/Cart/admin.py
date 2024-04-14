from django.contrib import admin
from .models import *

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product' , 'color' , 'size' , 'count' , 'created_at' , 'updated_at']
    readonly_fields = ['created_at' , 'updated_at']