"""Test for getting a vendor endpoint"""

import pytest
from django.urls import reverse
from utils.messages import MESSAGES


@pytest.mark.django_db
class TestGetAVendorEndpoint:
    """Test for getting a single vendor"""

    def test_get_a_vendor_succeeds(self, client, create_user, new_vendors):
        """Test get a new vendor endpoint"""

        vendor = new_vendors
        vendor_url = reverse('vendor:vendor-detail', args=[vendor[0].id])
        response = client.get(vendor_url)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['FETCHED'].format('Vendor')
        assert data['id'] == vendor[0].id
        assert data['name'] == vendor[0].name
        assert data['location'] == vendor[0].location
        assert data['email'] == vendor[0].email

    def test_get_a_vendor_fails(self, client, create_user, new_vendors):
        """Test get a new vendor endpoint"""

        vendor_url = reverse('vendor:vendor-detail', args=['invalid'])
        response = client.get(vendor_url)
        resp = response.data
        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

