from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html

UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        'last_login'
    ]

    add_form = UserCreationForm
    form = UserChangeForm
    model = UserModel
    list_display = ['username' , 'email', 'first_name', 'last_name' , 'phoneNumber' , 'is_superuser' , 'is_active' , 'level' , 'image_tag']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name' , 'phoneNumber' , 'image' , 'level')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phoneNumber', 'image' , 'level')}),
    )

    def image_tag(self, obj):
        if obj.image:
            img = obj.image.url
        else:
            img = 'https://i.pinimg.com/originals/51/f6/fb/51f6fb256629fc755b8870c801092942.png'

        return format_html('<img src="{}" width=50 />'.format(img))

    image_tag.short_description = 'image'

admin.site.register(UserModel, CustomUserAdmin)