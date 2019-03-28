"""Test for getting a vendor endpoint"""

import pytest
from django.urls import reverse
from utils.messages import MESSAGES


@pytest.mark.django_db
class TestGetAVendorEndpoint:
    """Test for getting a single vendor"""

    def vendor_url(self, vendor_id):
        """to generate vendor url"""
        return reverse('vendor:vendor-detail', args=[vendor_id])

    def test_get_a_vendor_succeeds(self, client, new_vendors):
        """Test get a new vendor endpoint"""

        vendor = new_vendors
        response = client.get(self.vendor_url(vendor[0].id))
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['FETCHED'].format('Vendor')
        assert data['id'] == vendor[0].id
        assert data['name'] == vendor[0].name
        assert data['location'] == vendor[0].location
        assert data['email'] == vendor[0].email

    def test_get_a_vendor_fails(self, client, new_vendors):
        """Test get a new vendor endpoint"""

        response = client.get(self.vendor_url('invalid'))
        resp = response.data
        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

