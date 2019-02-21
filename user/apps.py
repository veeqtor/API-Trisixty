from django.apps import AppConfig


class UserConfig(AppConfig):
    """Class representing the user application and its configuration."""

    name = 'user'

    def ready(self):
        """Imports the signals when Django starts"""

        import utils.signals
