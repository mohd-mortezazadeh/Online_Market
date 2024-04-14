from django.contrib import admin
from .models import *


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'amount', 'authority', 'ref_code' , 'created_at', 'updated_at'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]
