"""Module for product model test"""

import pytest

from tests.mocks.product_mock_data import NEW_PRODUCT


@pytest.mark.django_db
class TestProductModel:
    """Class representing the product model test"""

    def test_product_creation_success(self, create_product):
        """Test that vendors can be created"""

        product, _ = create_product
        assert product.title == NEW_PRODUCT['title']
        assert product.description == NEW_PRODUCT['description']
        assert product.images == NEW_PRODUCT['images']
        assert product.vendor == NEW_PRODUCT['vendor']

    def test_the_model_string_succeeds(self, create_product):
        """Test that vendors model string rep is correct."""

        product, _ = create_product

        assert product.__str__() == NEW_PRODUCT['title']

    def test_model_soft_delete_succeeds(self, create_product):
        """Test the soft delete"""

        product, _ = create_product

        product.delete()
        assert product.deleted is True

    def test_hard_delete(self, create_product):
        """Test for hard delete"""

        product, _ = create_product

        product.hard_delete()
        assert product.id is None






