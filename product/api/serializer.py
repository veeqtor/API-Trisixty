"""Module for the product serializer"""

from rest_framework import serializers

from product.models import Product
from vendor.api.serializer import VendorDetailsSerializer

from utils.constants import READ_ONLY_FIELDS


class ProductSerializer(serializers.ModelSerializer):
    """Class representing the vendor serializer"""

    vendor_detail = VendorDetailsSerializer(source='vendor', read_only=True)

    class Meta:
        """Meta"""

        model = Product

        fields = [
            'id',
            'title',
            'price',
            'description',
            'images',
            'vendor',
            'vendor_detail',
            'created_at',
            'updated_at'
        ]
        read_only_fields = READ_ONLY_FIELDS
        extra_kwargs = {
            "vendor": {
                "write_only": True,
                "error_messages": {
                    "does_not_exist":
                        "Vendor with the id '{pk_value}' does not exist."
                }
            },
            "price": {
                "error_messages": {
                    "invalid":
                        "'{value}' Value must include the Kobo denomination."
                }
            }
        }
