from django.db import models
from django.utils.translation import gettext_lazy as _


class GENDER_TYPE(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class COUNTRY_LIST(models.TextChoices):
    KENYA = "kenya", _("Kenya")
    TANZANIA = "tanzania", _("Tanzania")
    UGANDA = "uganda", _("Uganda")
    RWANDA = "rwanda", _("Rwanda")


class ROLES_TYPE(models.TextChoices):
    ADMIN = "admin", _("Admin")
    MANAGEMENT = "management", _("Management")
    SALES = "sales", _("Sales")
    CUSTOMER = "customer", _("Customer")
    UNDEFINED = "undefined", _("Undefined")
