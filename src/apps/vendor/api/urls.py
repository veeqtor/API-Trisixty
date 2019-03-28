"""Module for the vendor urls"""
from django.urls import path, include

from src.apps.vendor.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', views.VendorViewSet)

app_name = 'vendor'

urlpatterns = [
    path('vendors/', include(router.urls))
]
