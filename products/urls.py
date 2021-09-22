from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import OrderView, ProductView

app_name = "products"

# Register routes
router = DefaultRouter()
router.register("product", ProductView)
router.register("order", OrderView)

api_urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns = []
