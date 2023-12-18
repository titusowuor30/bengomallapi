from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import *
from django.contrib.auth import get_user_model
# Register your models here.
User=get_user_model()



class MyUserAdmin(UserAdmin):
    list_display = ('email', 'first_name','last_name','username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_superuser', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name','gender', 'pic', 'phone')}),
        ('Permissions', {'fields': ('email_confirm_token', 'user_permissions',
         'groups', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2','username','email', 'first_name','last_name', 'gender','pic','phone','groups','user_permissions','is_active','is_staff', 'is_superuser')}
        ),
    )
admin.site.register(MyUser,MyUserAdmin)
