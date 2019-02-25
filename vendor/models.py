from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.base_models import BaseAuditableModel
from user.models import User


class Vendor(BaseAuditableModel):
    """Model for vendors"""

    name = models.CharField(_('business Name'), max_length=255, unique=True)
    location = models.CharField(_('business Location'), max_length=255)
    description = models.TextField(_('business description'), blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo_url = models.CharField(_('logo URI'), max_length=255)
    email = models.EmailField(_('email'), max_length=50, unique=True)
    phone = models.CharField(_('phone'), max_length=20)

    class Meta:
        """Meta"""

        db_table = 'vendors'

    def __str__(self):
        """Output string"""

        return self.name
