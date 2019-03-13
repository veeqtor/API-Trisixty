"""Test for editing a product endpoint"""

import pytest
from django.urls import reverse

from utils.messages import MESSAGES

from tests.mocks.user_mock_data import NEW_USER, USER, NEW_USER_II
from tests.mocks.product_mock_data import NEW_PRODUCT_II


@pytest.mark.django_db
class TestEditAProductEndpoint:
    """Test for getting a single vendor"""

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def product_url(self, product_id):
        """Generates a url for products"""

        return reverse('product:product-detail', args=[product_id])

    def test_edit_a_product_succeeds(self, client, new_products,
                                     authenticate_user):
        """Test get a new product endpoint"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        product = new_products
        product_url = self.product_url(product[0].id)
        response = client.patch(product_url,
                                content_type='application/json',
                                data=NEW_PRODUCT_II, **auth_header)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['UPDATED'].format('Product')
        assert data['title'] == NEW_PRODUCT_II['title']
        assert data['description'] == NEW_PRODUCT_II['description']
        assert data['images'] == NEW_PRODUCT_II['images']

    def test_edit_a_product_by_supersuser_succeeds(self, client, new_products,
                                                   authenticate_user,
                                                   create_superuser):
        """Test get a new product endpoint"""

        create_superuser(USER)
        auth_header = self.authenticate_user(authenticate_user, USER)
        product = new_products
        product_url = self.product_url(product[0].id)
        response = client.patch(product_url,
                                content_type='application/json',
                                data=NEW_PRODUCT_II, **auth_header)
        resp = response.data
        data = resp['data']

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['UPDATED'].format('Product')
        assert data['title'] == NEW_PRODUCT_II['title']
        assert data['description'] == NEW_PRODUCT_II['description']
        assert data['images'] == NEW_PRODUCT_II['images']

    def test_editing_a_product_by_a_regular_user_fails(self, client,
                                                       create_user,
                                                       new_products,
                                                       authenticate_user):
        """Test get a new product endpoint"""
        create_user(NEW_USER_II)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER_II)
        product = new_products
        product_url = self.product_url(product[2].id)
        response = client.patch(product_url,
                                content_type='application/json',
                                data=NEW_PRODUCT_II, **auth_header)
        resp = response.data
        assert response.status_code == 403
        assert resp['status'] == 'error'
        assert resp == MESSAGES['NO_PERMISSION']

    def test_edit_a_product_created_by_another_vendor_fails(self, client,
                                                            verified_business_user,
                                                            new_products,
                                                            authenticate_user):
        """Test get a new product endpoint"""
        verified_business_user(NEW_USER_II)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER_II)
        product = new_products
        product_url = self.product_url(product[2].id)
        response = client.patch(product_url,
                                content_type='application/json',
                                data=NEW_PRODUCT_II, **auth_header)
        resp = response.data
        assert response.status_code == 403
        assert resp['status'] == 'error'
        assert resp == MESSAGES['NO_PERMISSION']

    def test_edit_an_invalid_product_fails(self, client,
                                           new_products,
                                           authenticate_user):
        """Test get a new product endpoint"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        product_url = self.product_url('Invalid')
        response = client.patch(product_url,
                                content_type='application/json',
                                data=NEW_PRODUCT_II, **auth_header)
        resp = response.data
        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_edit_a_product_with_an_already_existing_values_fails(self,
                                                                  client,
                                                                  new_products,
                                                                  authenticate_user):
        """Test get a new product endpoint"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        product = new_products
        product_url = self.product_url(product[0].id)
        response = client.patch(product_url,
                                content_type='application/json',
                                data={
                                    "title": product[1].title
                                }, **auth_header)
        resp = response.data
        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['errors']['title'][0] == MESSAGES['DUPLICATES'] \
            .format('Product', 'product title')
