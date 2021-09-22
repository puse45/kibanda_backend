from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import Customer

User = get_user_model()


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
        "last_login",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "role",
    )
    list_per_page = 20


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "sales_agent", "created_at")
    list_per_page = 20


admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
