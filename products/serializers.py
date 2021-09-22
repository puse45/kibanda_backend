from rest_framework import serializers

from accounts.choices import ROLES_TYPE
from accounts.serializers import UserDetailSerializer
from products.models import Orders, Products
from django.utils.translation import gettext_lazy as _

class ProductSerializer(serializers.ModelSerializer):
    created_by_detail = UserDetailSerializer(read_only=True,source="created_by")
    class Meta:
        model = Products
        fields = (
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "image",
            "country",
            "created_by",
            "created_by_detail",
        )

    def create(self, validated_date):
        return super().create(validated_date)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate(self, attrs):
        if not self.instance:
            created_by = attrs.get("created_by", None)
            if created_by.role not in [ROLES_TYPE.ADMIN,ROLES_TYPE.MANAGEMENT]:
                raise serializers.ValidationError(_("Sorry you are not allowed to post based from your role type"))
        return attrs


class OrdersSerializer(serializers.ModelSerializer):
    # onwer_detail
    customer_detail = UserDetailSerializer(read_only=True, source="customer")
    product_detail = ProductSerializer(read_only=True, source="product")
    class Meta:
        model = Orders
        fields = (
            "id",
            "product",
            "customer",
            "quantity",
            "customer_detail",
            "product_detail",
        )

    def create(self, validated_data):
        product = validated_data.get("product",None)
        quantity = validated_data.get("quantity",None)
        if product:
            product.update_remaining_stock(quantity=quantity)
        # return validated_data
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate(self, attrs):
        if not self.instance:
            quantity = attrs.get("quantity", None)
            customer = attrs.get("customer", None)
            product = attrs.get("product", None)
            if customer.role != ROLES_TYPE.CUSTOMER:
                raise serializers.ValidationError(_(f"Sorry your role must be a {ROLES_TYPE.CUSTOMER}"))
            if quantity > product.quantity:
                raise serializers.ValidationError(_(f"Sorry quantity can't be greater than {product.quantity}"))
        return attrs
