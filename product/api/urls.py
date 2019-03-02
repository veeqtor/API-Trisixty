"""Module for the product url"""

from django.urls import path, include

from product.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'', views.ProductViewSet)

app_name = 'product'

urlpatterns = [
    path('product/', include(router.urls))
]
