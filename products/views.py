from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Orders, Products
from products.serializers import OrdersSerializer, ProductSerializer


class ProductView(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["created_by"] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderView(ModelViewSet):
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(customer_id=self.request.user.id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data["customer"] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

