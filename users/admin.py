from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Calisan
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 
        'first_name',
        'last_name',
        'email', 
        'role', 
        'blok', 
        'kat', 
        'daire_no', 
        'uid', 
        'kirada_mi', 
        'mevcut_sakin', 
        'is_staff', 
        'is_active'
    )
    
    list_filter = (
        'role', 
        'kirada_mi', 
        'is_staff', 
        'is_active'
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Daire Bilgileri', {'fields': ('blok', 'kat', 'daire_no', 'uid', 'kirada_mi', 'mevcut_sakin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'blok', 'kat', 'daire_no', 'kirada_mi', 'mevcut_sakin', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)




class CalisanAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title')
    search_fields = ('user__username', 'job_title')