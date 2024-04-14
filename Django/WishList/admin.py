from django.contrib import admin
from .models import *

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product']

    readonly_fields = [
        'created_at',
        'updated_at'
    ]