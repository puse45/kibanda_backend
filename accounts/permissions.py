from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from rest_framework import permissions

User = get_user_model()


class IsSuperUser(permissions.BasePermission):
    """ Allow super_admin only """

    message = "You must be an Super User to access"

    def has_permission(self, request, view):
        user = request.user

        return request.user.is_authenticated and user.is_superuser


class IsAdmin(permissions.BasePermission):
    """ Allow supervisor only """

    message = "You must be an Admin to access"

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        elif user.is_superuser:  # Role names are lowercased
            return True

        return False


class IsGateKeeper(permissions.BasePermission):
    """ Allow gate keeper only """

    message = "You must be a Gate Keeper to access"

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        elif (
            user.is_superuser
            or (user.role.title == "admin".lower())
            or (user.role.title == "gate keeper".lower())
        ):
            return True

        return False


class IsDriver(permissions.BasePermission):
    """  Allow driver only """

    message = "You must be a Driver to access"

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        elif user.is_superuser or (user.role.title == "admin".lower()):
            return True
        elif user.role.title == "driver".lower():
            return True
        # TODO: Add check that allowed driver can only see their data

        return False


class IsAnalyst(permissions.BasePermission):
    """  Allow analysts only """

    message = "You must be an Analyst to access"

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        elif user.is_superuser or (user.role.title == "analyst".lower()):
            return True

        return False


class HasRole(permissions.BasePermission):
    """  Get user role only """

    def has_permission(self, request, view):
        user = request.user
        required_roles = getattr(view, "required_roles", None)

        if not user.is_authenticated:
            return False
        elif user.is_superuser:
            return True
        elif not required_roles:
            raise ImproperlyConfigured(
                "The HasRole permission requires adding a non empty list of required roles to the view class"
            )

        q = Q()
        for role in required_roles:
            q = q | Q(name__iexact=role)

        return user.roles.filter(q)


class OwnerOrModelPermission(permissions.BasePermission):
    def __same_user(self, obj, request):
        return isinstance(obj, User) and obj.id == request.user.id

    def __is_owner(self, obj, request):
        return (
            hasattr(obj, "owner")
            and obj.owner is not None
            and self.__same_user(obj.owner, request)
        )

    def has_permission(self, request, view):
        return request.user.is_superuser or permissions.BasePermission().has_permission(
            request, view
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or self.__same_user(obj, request)
            or self.__is_owner(obj, request)
            or permissions.BasePermission().has_object_permission(request, view, obj)
        )
