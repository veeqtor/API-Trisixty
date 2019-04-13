from django.apps import AppConfig
from django.db.models.signals import pre_save


class VendorConfig(AppConfig):
    """Class representing the vendor application and its configuration."""

    name = 'src.apps.vendor'

    def ready(self):
        """Generate push ID for the model"""

        from utils.signals import generate_push_id

        vendor_model = self.get_model('vendor')
        pre_save.connect(generate_push_id, sender=vendor_model)
