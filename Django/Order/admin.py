from django.contrib import admin
from .models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product' , 'color' , 'size' , 'count' , 'name',
                    'family', 'email' , 'phone' , 'address1' ,
                    'post_code', 'payment_type', 'status', 'created_at', 'updated_at']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]
