from django.contrib.auth import get_user_model
from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
User = get_user_model()


class BaseAdminPermission(permissions.BasePermission):
    """
    Global Base Database permission restrict non-admins from destroying data.
    """

    message = "Deleting content not allowed for this user type."

    def has_permission(self, request, view):
        # Logic to be implemented
        user = request.user
        if not user.is_active:
            return False
        if user.is_anonymous:
            return False
        return user.is_superuser or user.is_staff


class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    message = "Not allowed."

    def has_permission(self, request, view):
        # Logic to be implemented
        return True


class IsSuperuserOrIsSelf(permissions.BasePermission):
    """
    Permission for restricting creation of password.
    """

    message = "You've no permissions to change or create password."

    def has_permission(self, request, view):
        # Logic to be implemented
        return True


class IsSuperuser(permissions.BasePermission):
    """
    Permission for restricting creation of password.
    """

    message = "You've no permissions to change or create password."

    def has_permission(self, request, view):
        # Logic to be implemented
        user = request.user
        if not user.is_active:
            return False
        if user.is_anonymous:
            return False
        return user.is_superuser


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
