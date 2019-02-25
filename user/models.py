from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils import base_models
from utils.push_ID import PushID


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user
        Arguments:
            email (str): User email
        Keyword Arguments:
            password (str): User Password (default: (None))
        Returns:
            Object: User object
        """

        if not email:
            raise ValueError(_('Users must have an email address'))

        extra_fields['id'] = PushID().next_id()
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser

        Returns:
            Object: User object
        """

        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, base_models.BaseModel, PermissionsMixin):
    """Custom user model"""

    BUSINESS = 'BUSINESS'
    REGULAR = 'REGULAR'
    ACCOUNT_TYPE_CHOICES = (
        (BUSINESS, 'Business Account'),
        (REGULAR, 'Regular Account'),
    )

    email = models.EmailField(_('Email'), max_length=255, unique=True)
    first_name = models.CharField(_('First Name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    is_staff = models.BooleanField(_('Is staff'), default=False)
    verification_token = models.CharField(
        _('verification token'), max_length=100, blank=True, null=True)
    password_reset = models.CharField(
        _('Password reset token'), max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(_('Is verified'), default=False)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)
    account_type = models.CharField(
        _('Account type'),
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default=REGULAR,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def full_name(self):
        """Returns the fullname of the user"""
        return f'{self.first_name} {self.last_name}'

    class Meta:
        """Meta"""
        db_table = 'users'
