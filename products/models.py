import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.choices import COUNTRY_LIST
from base.models import BaseModel

User = get_user_model()


def get_product_image_dir(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join(
        "product", name, str(instance.name), " " + str(timezone.now())[:19] + ext
    )


class Products(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=False, null=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    image = models.ImageField(upload_to=get_product_image_dir, null=True, blank=True)
    country = models.CharField(
        max_length=15, choices=COUNTRY_LIST.choices, default=COUNTRY_LIST.KENYA
    )

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Orders(BaseModel):
    product = models.ForeignKey(
        Products, related_name="product_order", on_delete=models.PROTECT
    )
    customer = models.ForeignKey(
        User, related_name="customer_order", on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.product.name} - {self.customer}"

    # @property
    # def remaining_stock(self):
    #     remaining = self.product.quantity
    #     if remaining > 0:

    class Meta:
        ordering = ("-created_at",)
        get_latest_by = ("-created_at",)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
