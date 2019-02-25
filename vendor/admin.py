from django.contrib import admin
from vendor.models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Vendor admin"""

    ordering = ['id']
    list_display = ['name', 'email', 'location']
    list_display_links = ['email']
    search_fields = ['name', 'location', 'email']
    list_per_page = 25

    fieldsets = (
        (None, {
            'classes': ('small',),
            'fields': (
                'name',
                'email',
                'owner',
                'logo_url',
                'location',
                'phone',
                'description'
            ),
        }),
    )

