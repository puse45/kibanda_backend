import logging

from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.choices import ROLES_TYPE
from accounts.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserDetailSerializer,
    userSerializer,
)

# Create your views here.

User = get_user_model()
logger = logging.getLogger(__file__)


class RegisterCustomerView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["role"] = ROLES_TYPE.CUSTOMER
        data["user_type"] = self.request.user.id.hex
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserDetailSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "Account created successfully. Use received token to activate your account.",
            }
        )


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserDetailSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "Account created successfully. Use received token to activate your account.",
            }
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
        return Response(
            {"error": "Unable to login"}, status=status.HTTP_400_BAD_REQUEST
        )


class UsersView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = userSerializer
    queryset = User.objects.all()
    permission_classes = IsAuthenticated
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("email", "id")

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
