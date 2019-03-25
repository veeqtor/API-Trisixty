"""Module to test the sideloading vendors and owners"""

import pytest
from django.urls import reverse

from utils.messages import MESSAGES
from tests.mocks.vendor_mock_data import NEW_VENDOR
from tests.mocks.user_mock_data import NEW_USER

PRODUCT_LIST = reverse('product:product-list')


@pytest.mark.django_db
class TestSideLoadingVendorsAndOwners:
    """Test class for endpoints to get products"""

    def product_url(self, product_id):
        """To generate product url"""

        return reverse('product:product-detail', args=[product_id])

    def test_get_all_products_with_vendor_details_succeeds(self, client,
                                                           new_products):
        """test to test the get all endpoint"""

        response = client.get(PRODUCT_LIST + '?include=vendor')
        resp = response.data
        data = resp['data'][0]['vendor_detail']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['FETCHED'].format('Products')
        assert data['name'] == NEW_VENDOR['name']
        assert data['location'] == NEW_VENDOR['location']
        assert data['description'] == NEW_VENDOR['description']
        assert isinstance(data['owner'], str)

    def test_get_all_products_with_vendor_details_and_owner_succeeds(self,
                                                                     client,
                                                                     new_products):
        """test to test the get all endpoint"""

        response = client.get(PRODUCT_LIST + '?include=vendor,owner')
        resp = response.data
        resp_data = resp['data'][0]
        data = resp['data'][0]['vendor_detail']['owner']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['FETCHED'].format('Products')
        assert data['email'] == NEW_USER['email']
        assert data['first_name'] == NEW_USER['first_name']
        assert data['last_name'] == NEW_USER['last_name']
        assert isinstance(resp_data['vendor_detail'], dict)

