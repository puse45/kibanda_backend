import requests
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import LoginView, RegisterCustomerView, RegistrationView, UsersView, TotalCustomers
from .viewsets import UserViewSet

app_name = "accounts"

# Register routes
router = DefaultRouter()
router.register("users", UserViewSet)

api_urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path(
        "register/customer/", RegisterCustomerView.as_view(), name="register_customer"
    ),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
    path("user/", UsersView.as_view(), name="Users"),
    path("all/customers", TotalCustomers.as_view(), name="total_customers"),
]

urlpatterns = []
