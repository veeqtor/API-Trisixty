"""Module for vendor model test"""

import pytest

from tests.mocks.vendor_mock_data import NEW_VENDOR


@pytest.mark.django_db
class TestVendorModel:
    """Class representing the vendor model test"""

    def test_vendor_creation_success(self, create_user, create_vendor):
        """Test that vendors can be created"""

        vendor = create_vendor

        assert vendor.name == NEW_VENDOR['name']
        assert vendor.description == NEW_VENDOR['description']
        assert vendor.location == NEW_VENDOR['location']
        assert vendor.owner == NEW_VENDOR['owner']
        assert vendor.email == NEW_VENDOR['email']

    def test_the_model_string_succeeds(self, create_user, create_vendor):
        """Test that vendors model string rep is correct."""

        vendor = create_vendor

        assert vendor.__str__() == NEW_VENDOR['name']

    def test_model_soft_delete_succeeds(self, create_user, create_vendor):
        """Test the soft delete"""

        vendor = create_vendor

        vendor.delete()
        assert vendor.deleted is True

    def test_hard_delete(self, create_user, create_vendor):
        """Test for hard delete"""

        vendor = create_vendor

        vendor.hard_delete()
        assert vendor.id is None






