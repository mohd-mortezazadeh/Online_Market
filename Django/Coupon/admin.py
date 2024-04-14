from django.contrib import admin
from .models import *

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [ "code","percent","uses_number","expiration","user","created_at","updated_at" ]
    readonly_fields = ['created_at' , 'updated_at']