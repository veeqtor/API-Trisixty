"""Module Sending emails to users"""

from django.contrib.auth import get_user_model
from django.template.loader import get_template

from services.email import send


class UserSend:
    """class for User emails"""

    @classmethod
    def verification_email(cls, user_id):
        """Sends out user verification email.

        Args:
            user_id (str): User's id

        Returns:
            None

        """

        subject = 'Verification Link'
        found_user = cls.find_user(user_id)
        template = get_template('verification_email.html')
        ctx = {'token': found_user.verification_token}
        html_content = template.render(ctx)

        send.delay(subject, found_user.email, html_content)

    @classmethod
    def password_reset_email(cls, user_id):
        """Sends out user password reset email.

        Args:
            user_id: User's id

        Returns:
            None

        """

        subject = 'Password Reset'
        found_user = cls.find_user(user_id)
        template = get_template('password_reset.html')
        ctx = {'token': found_user.password_reset}
        html_content = template.render(ctx)

        send.delay(subject, found_user.email, html_content)

    @classmethod
    def find_user(cls, id):
        """Finds user form the database.

        Args:
            id (str): User id

        Returns:
            Object: The user object.

        """

        user = get_user_model()
        return user.objects.filter(pk=id).first()
