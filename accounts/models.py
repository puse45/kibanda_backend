import os

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.choices import COUNTRY_LIST, GENDER_TYPE, ROLES_TYPE
from accounts.managers import UserManager
from base.models import BaseModel


def get_user_profile_photos_dir(instance, filename):
    f_name, ext = os.path.splitext(filename)
    return os.path.join(
        "profiles",
        "photos",
        str(instance.phone_number),
        " " + str(timezone.now())[:19] + ext,
    )


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Account.User model overrides the builtin auth.User model.
    Attributes:
        @:param sur_name                    :   user's sur name.
        @:param first_name                  :   user's first name.
        @:param last_name                   :   user's last name.
        @:param password                    :   user's password.
        @:param is_password_changed         :   whether user has changed default password or not. Merchants will create
         users with this field set to False.
    """

    sur_name = models.CharField(
        max_length=100, help_text=_("Enter surname."), null=False, blank=False
    )
    first_name = models.CharField(
        max_length=100, help_text=_("Enter first name."), null=False, blank=False
    )
    last_name = models.CharField(
        max_length=100, help_text=_("Enter last name."), null=False, blank=False
    )
    email = models.EmailField(
        max_length=200, help_text=_("Enter an email address."), null=True, blank=True
    )
    phone_number = models.CharField(unique=True, max_length=15, null=True, blank=True)
    gender = models.CharField(
        max_length=8, choices=GENDER_TYPE.choices, default=GENDER_TYPE.MALE
    )
    profile_photo = models.ImageField(
        upload_to=get_user_profile_photos_dir, null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=15, choices=ROLES_TYPE.choices, default=ROLES_TYPE.UNDEFINED
    )
    country = models.CharField(
        max_length=15, choices=COUNTRY_LIST.choices, default=COUNTRY_LIST.KENYA
    )
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_login = models.DateTimeField(_("last login"), default=timezone.now)
    slug = None
    objects = UserManager()

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def full_name(self):
        return f"{self.sur_name} {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.first_name}"

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Customer(BaseModel):
    customer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="customer_user"
    )
    sales_agent = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="sales_agent_user"
    )
    slug = None

    def __str__(self):
        return f"Customer {self.customer.get_full_name}"

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
