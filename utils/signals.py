"""Models for signals"""
from utils.push_ID import PushID
from tasks.user_emails import UserSend


def generate_push_id(sender, instance, **kwargs):
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
