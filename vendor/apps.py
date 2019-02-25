from django.apps import AppConfig
from django.db.models.signals import pre_save


class VendorConfig(AppConfig):
    """Class representing the vendor application and its configuration."""

    name = 'vendor'

    def ready(self):
        """Generate push ID for the model"""

        from utils.signals import generate_push_id
        from .models import Vendor

        pre_save.connect(generate_push_id, sender=Vendor)
