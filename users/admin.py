from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdminConfig(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    list_display = ['email','username', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields':('email', 'username', )}),
        ('Permissions', {'fields':('is_staff', 'is_active', )}),
        )

    add_fieldsets = (
        (None, {'fields':('email', 'username', 'password1', 'password2')}),
        ('Permissions', {'fields':('is_staff', 'is_active',)}),
        )
    
        
admin.site.register(CustomUser, CustomUserAdminConfig)
