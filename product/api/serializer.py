"""Module for the product serializer"""

from rest_framework import serializers

from product.models import Product
from vendor.api.serializer import VendorDetailsSerializer


class ProductSerializer(serializers.ModelSerializer):
    """Class representing the vendor serializer"""

    class Meta:
        """Meta"""

        model = Product
        vendor = VendorDetailsSerializer()
        fields = [
            'id',
            'title',
            'price',
            'description',
            'images',
            'vendor',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            "vendor": {
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
