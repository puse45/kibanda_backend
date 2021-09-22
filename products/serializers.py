from rest_framework import serializers

from products.models import Orders, Products


class ProductSerializer(serializers.ModelSerializer):
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
        )

    def create(self, validated_date):
        return super().create(validated_date)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            "id",
            "product",
            "customer",
            "quantity",
        )

    def create(self, validated_date):
        return super().create(validated_date)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
