"""Module to test the delete endpoint"""

import pytest
from django.urls import reverse
from utils.messages import MESSAGES
from vendor.models import Vendor

from tests.mocks.user_mock_data import NEW_USER


@pytest.mark.django_db
class TestDeleteEndpoint:
    """Class representing the delete endpoint tests."""

    def vendor_url(self, vendor_id, type):
        """to generate vendor url"""
        mapper = {
            'soft': 'vendor:vendor-detail',
            'hard': 'vendor:vendor-hard-delete',
            'restore': 'vendor:vendor-restore'
        }
        return reverse(mapper[type], args=[vendor_id])

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_deleting_a_vendor_succeeds(self, client, create_user,
                                        authenticate_user, new_vendors):
        """Test that deleting a vendor succeeds"""

        vendor = new_vendors
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.vendor_url(vendor[0].id, 'soft'),
                                 **auth_header)
        updated_vendors = Vendor.objects.filter(id=vendor[0].id).first()
        resp = response.data

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['DELETED'].format('Vendor')
        assert updated_vendors.deleted

    def test_deleting_already_soft_deleted_vendor_fails(self, client,
                                                        create_user,
                                                        authenticate_user,
                                                        new_vendors):
        """Test that deleting a vendor succeeds"""

        vendor = new_vendors
        vendor[0].deleted = True
        vendor[0].save()
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.vendor_url(vendor[0].id, 'soft'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_restore_a_nonexistent_vendor_fails(self, client, create_user,
                                                authenticate_user,
                                                new_vendors):
        """Test that deleting a vendor succeeds"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(self.vendor_url('invalid', 'restore'),
                              **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_restoring_a_deleted_vendor_succeeds(self, client, create_user,
                                                 authenticate_user,
                                                 new_vendors):
        """Test that deleting a vendor succeeds"""

        vendor = new_vendors
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(self.vendor_url(vendor[0].id, 'restore'),
                              **auth_header)
        resp = response.data

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['RESTORE'].format('Vendor',
                                                             vendor[0].name)

    def test_soft_deleting_a_nonexistent_vendor_fails(self, client, create_user,
                                                      authenticate_user,
                                                      new_vendors):
        """Test that deleting a vendor succeeds"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.vendor_url('invalid', 'soft'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_hard_deleting_a_vendor_succeeds(self, client, create_user,
                                             authenticate_user,
                                             new_vendors):
        """Test that deleting a vendor succeeds"""

        vendor = new_vendors
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.vendor_url(vendor[0].id, 'hard'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['P_DELETED'].format('Vendor')

    def test_hard_deleting_a_nonexistent_vendor_fails(self, client, create_user,
                                                      authenticate_user,
                                                      new_vendors):
        """Test that deleting a vendor succeeds"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.vendor_url('invalid', 'hard'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']
