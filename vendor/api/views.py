"""Module for the views"""
from rest_framework import viewsets

from vendor.models import Vendor
from vendor.api.serializer import VendorSerializer


class VendorViewSet(viewsets.ModelViewSet):
        """A viewset for viewing and editing vendor instances."""

        serializer_class = VendorSerializer
        queryset = Vendor.objects.all()
