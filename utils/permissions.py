"""Permissions Module"""

from rest_framework.permissions import BasePermission
from .messages import MESSAGES


class VerifiedBusinessAccountPermission(BasePermission):
    """Permission class for verified business accounts"""

    message = MESSAGES['NO_PERMISSION']

    def has_permission(self, request, view):
        """Allows access only to verified and business account users."""

        user = request.user

        return bool(user.is_superuser or
                    (user.is_verified and user.account_type == 'BUSINESS'))

    def has_object_permission(self, request, view, obj):
        """Does the object has permission"""

        is_owner = bool(obj.owner == request.user)
        is_superuser = bool(request.user.is_superuser)

        return bool(is_superuser or is_owner)


class IsAuthenticated(BasePermission):
    """Allows access only to authenticated users."""

    message = MESSAGES['NO_PERMISSION']

    def has_permission(self, request, view):
        """Checks for the permission"""

        return bool(request.user and request.user.is_authenticated)
