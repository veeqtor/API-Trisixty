"""Module to test the create product endpoint"""

import pytest

from django.urls import reverse

from tests.mocks.user_mock_data import NEW_USER, USER
from tests.mocks.product_mock_data import NEW_PRODUCT

from utils.messages import MESSAGES

PRODUCT_URL = reverse('product:product-list')


@pytest.mark.django_db
class TestCreateProductEndpoint:
    """Test the product creation endpoints."""

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_create_product_without_permissions_fails(self, client, create_user,
                                                      authenticate_user):
        """Test that vendor creations succeeds"""

        create_user(NEW_USER)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)

        response = client.post(PRODUCT_URL, data=NEW_PRODUCT, **auth_header)
        resp = response.data

        assert response.status_code == 403
        assert resp == MESSAGES['NO_PERMISSION']

    def test_create_product_without_vendor_fails(self, client, create_user,
                                                 authenticate_user):
        user = create_user(NEW_USER)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()

        response = client.post(PRODUCT_URL, data=NEW_PRODUCT, **auth_header)
        resp = response.data

        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['errors']['vendor_id'][0] == MESSAGES['REQUIRED_FIELD']

    def test_create_product_for_another_vendor_fails(self, client, create_user,
                                                     authenticate_user,
                                                     create_vendor):
        vendor, _ = create_vendor
        NEW_PRODUCT['vendor_id'] = vendor.id

        user = create_user(NEW_USER)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()

        response = client.post(PRODUCT_URL, data=NEW_PRODUCT, **auth_header)
        resp = response.data

        assert response.status_code == 403
        assert resp == MESSAGES['NO_PERMISSION']

    def test_create_product_succeeds(self, client,
                                     authenticate_user, create_vendor):
        vendor, user = create_vendor
        NEW_PRODUCT['vendor_id'] = vendor.id

        auth_header = self.authenticate_user(authenticate_user, USER)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()

        response = client.post(PRODUCT_URL, data=NEW_PRODUCT, **auth_header)
        resp = response.data

        assert response.status_code == 201
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['CREATED'].format('Product')

    def test_create_already_exiting_product_fails(self, client, create_vendor,
                                                  authenticate_user,
                                                  create_product):
        vendor, user = create_vendor

        NEW_PRODUCT['vendor_id'] = vendor.id

        auth_header = self.authenticate_user(authenticate_user, USER)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()

        response = client.post(PRODUCT_URL, data=NEW_PRODUCT, **auth_header)
        resp = response.data

        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['errors']['title'][0] == MESSAGES['DUPLICATES'] \
            .format('Product', 'product title')
