"""Module for the vendor serializer"""

from rest_framework import serializers

from vendor.models import Vendor
from user.api.serializers import DetailedUserSerializer

from utils.constants import READ_ONLY_FIELDS


class VendorSerializer(serializers.ModelSerializer):
    """Class representing the vendor serializer"""

    class Meta:
        """Meta"""

        model = Vendor
        fields = [
            'id',
            'name',
            'location',
            'description',
            'owner',
            'logo_url',
            'email',
            'phone',
            'created_at',
            'updated_at'
        ]
        read_only_fields = READ_ONLY_FIELDS + ['owner']
        extra_kwargs = {
            "owner": {
                "error_messages": {
                    "does_not_exist":
                        "Owner with the id '{pk_value}' does not exist."
                }
            }
        }


class VendorDetailsSerializer(VendorSerializer):
    """Serializer for a single vendor"""

    owner = DetailedUserSerializer()
