"""Test module for the create endpoint"""

import pytest
from tests.mocks.user_mock_data import NEW_USER, USER
from tests.mocks.vendor_mock_data import NEW_VENDOR
from utils.messages import MESSAGES

VENDOR_URL = '/api/v1/vendor/'


@pytest.mark.django_db
class TestCreateVendorEndpoint:
    """Test the vendor creation endpoints."""

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_create_vendor_fails(self, client, create_user, authenticate_user):
        """Test that vendor creations succeeds"""

        create_user(NEW_USER)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)

        response = client.post(VENDOR_URL, data=NEW_VENDOR, **auth_header)
        resp = response.data

        assert response.status_code == 403
        assert resp['status'] == MESSAGES['NO_PERMISSION']['status']
        assert resp['errors'] == MESSAGES['NO_PERMISSION']['errors']
        assert resp == MESSAGES['NO_PERMISSION']

    def test_create_vendor_succeeds(self, client, create_user,
                                    authenticate_user):
        user = create_user(NEW_USER)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()

        response = client.post(VENDOR_URL, data=NEW_VENDOR, **auth_header)
        resp = response.data

        assert response.status_code == 201
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['CREATED'].format('Vendor')

    def test_create_already_exiting_vendor_fails(self,
                                                 client,
                                                 create_vendor,
                                                 authenticate_user):
        vendor, user = create_vendor
        auth_header = self.authenticate_user(authenticate_user, USER)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()

        response = client.post(VENDOR_URL, data=NEW_VENDOR, **auth_header)
        resp = response.data

        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['errors']['name'][0] == MESSAGES['DUPLICATES'] \
            .format('vendor', 'business name')
        assert resp['errors']['email'][0] == MESSAGES['DUPLICATES'] \
            .format('vendor', 'email')
