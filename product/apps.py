
from django.apps import AppConfig
from django.db.models.signals import pre_save


class ProductConfig(AppConfig):
    """Class representing the vendor application and its configuration."""

    name = 'product'

    def ready(self):
        """Generate push ID for the model"""

        from utils.signals import generate_push_id
        from .models import Product

        pre_save.connect(generate_push_id, sender=Product)
