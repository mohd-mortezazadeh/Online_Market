from django.contrib import admin
from .models import *

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['title' , 'label']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title' , 'label']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Role_User)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role' , 'user']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Role_Permission)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role' , 'permission']
    readonly_fields = ['created_at', 'updated_at']