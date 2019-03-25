"""Module for the product serializer"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from product.models import Product
from utils.messages import MESSAGES
from vendor.api.serializer import VendorSerializer, VendorDetailsSerializer
from vendor.models import Vendor


from utils.constants import READ_ONLY_FIELDS


class ProductSerializer(serializers.ModelSerializer):
    """Class representing the vendor serializer"""

    vendor_id = serializers.PrimaryKeyRelatedField(
            queryset=Vendor.objects.all(), source='vendor',
            error_messages={
                    "does_not_exist":
                    "Vendor with the id '{pk_value}' does not exist."
                })

    title = serializers.CharField(max_length=255, validators=[
        UniqueValidator(queryset=Product.objects.filter(deleted=False).all(),
                        message=MESSAGES['DUPLICATES'].format('Product',
                                                              'product title'))
    ])

    class Meta:
        """Meta"""

        model = Product

        fields = [
            'id',
            'title',
            'price',
            'description',
            'availability',
            'images',
            'vendor_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = READ_ONLY_FIELDS
        extra_kwargs = {
            "price": {
                "error_messages": {
                    "invalid":
                        "'{value}' Value must include the Kobo denomination."
                }
            }
        }


class ProductWithVendorSerializer(ProductSerializer):
    """Serializer for side-loading vendors"""

    vendor_detail = VendorSerializer(source='vendor', read_only=True)

    class Meta(ProductSerializer.Meta):
        """Meta"""

        fields = ProductSerializer.Meta.fields.copy()
        fields.pop(6)
        fields.extend(['vendor_detail'])


class ProductWithOwnerSerializer(ProductWithVendorSerializer):
    """Serializer for side-loading owner"""

    vendor_detail = VendorDetailsSerializer(source='vendor', read_only=True)

