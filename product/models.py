"""Module representing the product model."""

from django.db import models

from django.contrib.postgres import fields

from utils.base_models import BaseAuditableModel
from django.utils.translation import gettext_lazy as _
from vendor.models import Vendor


class Product(BaseAuditableModel):
    """Class representing the product model class"""

    title = models.CharField(_('Product name'), max_length=255, unique=True)
    price = models.FloatField(_('Product price'))
    images = fields.ArrayField(
            models.CharField(_('Image URI'),
                             default=['https://placehold.it/500X500'],
                             max_length=255
                             ))
    description = models.TextField(_('Product description'))
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
        """Meta"""

        ordering = ('-created_at',)
        db_table = 'products'

    def __str__(self):
        """Output string"""

        return self.title
