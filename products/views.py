from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from products.models import Orders, Products
from products.serializers import OrdersSerializer, ProductSerializer


class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    permission_classes = (IsAuthenticated,)


class OrderView(ModelViewSet):
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(customer_id=self.request.user.id)
        return self.queryset
