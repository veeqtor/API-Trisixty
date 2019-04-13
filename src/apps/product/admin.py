from django.contrib import admin
from src.apps.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin"""

    ordering = ['id']
    list_display = ['title', 'price', 'vendor', 'description']
    list_display_links = ['title']
    search_fields = ['title', 'vendor', 'price']
    list_per_page = 25

    fieldsets = (
        (None, {
            'classes': ('small',),
            'fields': (
                'title',
                'price',
                'vendor',
                'images',
                'description'
            ),
        }),
    )

