"""Test for editing a vendor endpoint"""

import pytest
from django.urls import reverse

from utils.messages import MESSAGES

from tests.mocks.user_mock_data import NEW_USER, USER
from tests.mocks.vendor_mock_data import NEW_VENDOR_II


@pytest.mark.django_db
class TestEditAVendorEndpoint:
    """Test for getting a single vendor"""

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_edit_a_vendor_succeeds(self, client, new_vendors,
                                    authenticate_user):
        """Test get a new vendor endpoint"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        vendor = new_vendors
        vendor_url = reverse('vendor:vendor-detail', args=[vendor[0].id])
        response = client.patch(vendor_url,
                                content_type='application/json',
                                data=NEW_VENDOR_II, **auth_header)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['UPDATED'].format('Vendor')
        assert data['name'] == NEW_VENDOR_II['name']
        assert data['location'] == NEW_VENDOR_II['location']
        assert data['email'] == NEW_VENDOR_II['email']

    def test_edit_a_vendor_created_by_another_user_fails(self, client,
                                                         create_user,
                                                         new_vendors,
                                                         authenticate_user):
        """Test get a new vendor endpoint"""

        create_user(USER)
        auth_header = self.authenticate_user(authenticate_user, USER)
        vendor = new_vendors
        vendor_url = reverse('vendor:vendor-detail', args=[vendor[2].id])
        response = client.patch(vendor_url,
                                content_type='application/json',
                                data=NEW_VENDOR_II, **auth_header)
        resp = response.data
        assert response.status_code == 403
        assert resp['status'] == 'error'
        assert resp == MESSAGES['NO_PERMISSION']

    def test_edit_a_non_existent_vendor_fails(self, client,
                                              new_vendors,
                                              authenticate_user):
        """Test get a new vendor endpoint"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        vendor_url = reverse('vendor:vendor-detail', args=['invalid'])
        response = client.patch(vendor_url,
                                content_type='application/json',
                                data=NEW_VENDOR_II, **auth_header)
        resp = response.data
        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_edit_a_vendor_with_an_already_existing_values_fails(self,
                                                                 client,
                                                                 new_vendors,
                                                                 authenticate_user):
        """Test get a new vendor endpoint"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        vendor = new_vendors
        vendor_url = reverse('vendor:vendor-detail', args=[vendor[0].id])
        response = client.patch(vendor_url,
                                content_type='application/json',
                                data={
                                    "name": vendor[1].name
                                }, **auth_header)
        resp = response.data
        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['errors']['name'][0] == MESSAGES['DUPLICATES'] \
            .format('vendor', 'business name')
