"""Models for signals"""

from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from utils.push_ID import PushID
from tasks.user_emails import UserSend


user = get_user_model()

models = [
    user
]


for model in models:
    @receiver(pre_save, sender=model)
    def push_id(sender, instance, **kwargs):
        """Generates push id before anything is saved to the database.

        Args:
            sender (object): The model class.
            instance (object): The actual instance being saved.
            **kwargs:

        Returns:
            None

        """

        push_id = PushID().next_id()
        if len(instance.id) < 20 or instance.id is None:
            instance.id = push_id


@receiver(post_save, sender=user)
def send_verification_email(sender, instance, created, **kwargs):
    """Send out user verification

    Args:
        sender (object): The model class.
        instance (object): The actual instance being saved.
        created (bool): True if a new record was created.
        **kwargs:

    Returns:
        None

    """

    if created and not instance.is_verified:
        # Send verification email
        UserSend.verification_email(instance.pk)
