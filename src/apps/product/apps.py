
from django.apps import AppConfig
from django.db.models.signals import pre_save


class ProductConfig(AppConfig):
    """Class representing the vendor application and its configuration."""

    name = 'src.apps.product'

    def ready(self):
        """Generate push ID for the model"""

        from utils.signals import generate_push_id

        product_model = self.get_model('product')
        pre_save.connect(generate_push_id, sender=product_model)
