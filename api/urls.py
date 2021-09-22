from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.urls import api_urlpatterns as account_urls
from products.urls import api_urlpatterns as products_urls

app_name = "api"

router = DefaultRouter()

urlpatterns = [
    path("accounts/", include(account_urls)),
    path("", include(products_urls)),
]
