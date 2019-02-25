"""Module for the vendor urls"""

from vendor.api.views import VendorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', VendorViewSet, basename='vendor')
urlpatterns = router.urls
