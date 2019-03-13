"""Module for the vendor get endpoint"""

import pytest
from django.urls import reverse

from tests.mocks.user_mock_data import NEW_USER, USER

from utils.messages import MESSAGES

VENDOR_URL = reverse('vendor:vendor-list')


@pytest.mark.django_db
class TestGetAllVendorEndpoint:
    """Class representing test for get all vendors"""

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_only_authenticated_user(self, client):
        """Test only authenticated users can access"""

        response = client.get(VENDOR_URL)
        assert response.status_code == 401
        assert response.data['detail'] == \
            'Authentication credentials were not provided.'

    def test_get_all_vendors_succeeds(self, client, authenticate_user,
                                      new_vendors):
        """Test the get all vendors endpoint."""

        vendors = new_vendors
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(VENDOR_URL, **auth_header)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert len(data) == 4
        assert resp['meta']['count'] == 4
        assert data[0]['name'] == vendors[-1].name
        assert data[-1]['name'] == vendors[0].name

    def test_get_all_vendors_invalid_page_succeeds(self, client,
                                                   authenticate_user,
                                                   new_vendors):
        """Test the get all vendors endpoint."""
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(VENDOR_URL + "?page=5", **auth_header)
        resp = response.data
        data = resp['data']

        assert response.status_code == 404
        assert data == []
        assert resp['message'] == MESSAGES['INVALID_PAGE']

    def test_get_all_vendors_fails(self, client, create_user, authenticate_user,
                                   new_vendors):
        """Test the get all vendors endpoint."""

        create_user(USER)
        auth_header = self.authenticate_user(authenticate_user, USER)
        response = client.get(VENDOR_URL, **auth_header)
        resp = response.data

        assert response.status_code == 403
        assert resp == MESSAGES['NO_PERMISSION']

    def test_get_all_vendors_after_soft_delete(self, client,
                                               authenticate_user, new_vendors):
        vendors = new_vendors
        vendors[0].deleted = True
        vendors[0].save()
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(VENDOR_URL, **auth_header)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert len(data) == 3
        assert resp['meta']['count'] == 3
        assert data[0]['name'] == vendors[-1].name
