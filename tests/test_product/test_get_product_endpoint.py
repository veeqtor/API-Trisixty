"""Module to test the get product endpoints"""

import pytest
from django.urls import reverse

from utils.messages import MESSAGES

PRODUCT_LIST = reverse('product:product-list')


@pytest.mark.django_db
class TestGetProductEndpoint:
    """Test class for endpoints to get products"""

    def product_url(self, product_id):
        """To generate product url"""

        return reverse('product:product-detail', args=[product_id])

    def test_get_all_products_succeeds(self, client, new_products):
        """test to test the get all endpoint"""

        products = new_products

        response = client.get(PRODUCT_LIST)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['FETCHED'].format('Products')
        assert data[0]['id'] == products[-1].id
        assert data[0]['title'] == products[-1].title
        assert data[0]['price'] == products[-1].price
        assert data[0]['description'] == products[-1].description

    def test_get_all_products_with_invalid_page_fails(self, client,
                                                      new_products):
        """test to test the get all endpoint"""

        response = client.get(PRODUCT_LIST + '?page=100')
        resp = response.data
        data = resp['data']

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['INVALID_PAGE']
        assert data == []

    def test_get_a_product_succeeds(self, client, new_products):
        """Test the get a product endpoint"""

        products = new_products
        product_detail_url = self.product_url(products[0].id)
        response = client.get(product_detail_url)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['FETCHED'].format('Product')
        assert data['id'] == products[0].id
        assert data['title'] == products[0].title
        assert data['price'] == products[0].price
        assert data['description'] == products[0].description

    def test_get_a_product_fails(self, client, new_products):
        """Test the get a product endpoint"""

        product_detail_url = self.product_url('invalid-id')
        response = client.get(product_detail_url)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']
