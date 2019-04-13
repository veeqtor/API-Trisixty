"""Module for the vendor serializer"""

from rest_framework import serializers

from src.apps.vendor.models import Vendor
from src.apps.user.api.serializers import DetailedUserSerializer

from utils.constants import READ_ONLY_FIELDS


class VendorSerializer(serializers.ModelSerializer):
    """Class representing the vendor serializer"""

    logoUrl = serializers.CharField(source='logo_url', required=False)
    createdAt = serializers.CharField(source='created_at', read_only=True)
    updatedAt = serializers.CharField(source='updated_at', read_only=True)

    class Meta:
        """Meta"""

        model = Vendor
        fields = [
            'id',
            'name',
            'location',
            'description',
            'owner',
            'logoUrl',
            'email',
            'phone',
            'createdAt',
            'updatedAt'
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
