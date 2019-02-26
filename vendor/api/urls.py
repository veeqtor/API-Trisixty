"""Module for the vendor urls"""

from vendor.api.views import VendorView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'vendor', VendorView, basename='vendor')
urlpatterns = router.urls
