"""Module for the vendor urls"""
from django.urls import path, include

from vendor.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', views.VendorView)

app_name = 'vendor'

urlpatterns = [
    path('vendor/', include(router.urls))
]
