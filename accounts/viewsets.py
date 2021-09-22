import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdmin
from accounts.serializers import userSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = userSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        else:
            return self.queryset.filter(pk=user.id)
