from django.contrib import admin

# Register your models here.
from products.models import Orders, Products


class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "country", "created_at", "updated_at")
    search_fields = (
        "name",
        "country",
        "price",
    )
    list_per_page = 20


class OrdersAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "quantity", "created_at", "updated_at")
    search_fields = (
        "product",
        "quantity",
    )
    list_per_page = 20


admin.site.register(Products, ProductsAdmin)
admin.site.register(Orders, OrdersAdmin)
