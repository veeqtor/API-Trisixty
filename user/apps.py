from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model


class UserConfig(AppConfig):
    """Class representing the user application and its configuration."""

    name = 'user'

    def ready(self):
        """Imports the signals and connect when Django starts"""

        from utils.signals import generate_push_id, send_verification_email

        user = get_user_model()

        pre_save.connect(generate_push_id, sender=user)
        post_save.connect(send_verification_email, sender=user)
