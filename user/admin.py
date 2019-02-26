from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """custom admin for the user model"""

    ordering = ['id']
    list_display = ['email', 'full_name', 'account_type', 'is_verified',
                    'date_joined', 'is_staff', 'is_superuser']
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'account_type',
                'is_verified'
            )
        }),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name'
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    # 'groups',
                    # 'user_permissions'
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined'
                )
            }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
