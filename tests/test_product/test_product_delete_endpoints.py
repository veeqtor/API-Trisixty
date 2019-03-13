"""Module for product delete endpoint test."""

import pytest
from django.urls import reverse

from product.models import Product
from tests.mocks.user_mock_data import NEW_USER, USER
from utils.messages import MESSAGES


@pytest.mark.django_db
class TestDeleteEndpoints:
    """Class to test for the product delete endpoints"""

    def product_url(self, vendor_id, type):
        """to generate product url"""

        mapper = {
            'soft': 'product:product-detail',
            'hard': 'product:product-hard-delete',
            'restore': 'product:product-restore'
        }
        return reverse(mapper[type], args=[vendor_id])

    def authenticate_user(self, authenticate_user, user):
        """Authenticates users"""

        token = authenticate_user(user)
        return {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }

    def test_soft_deleting_a_product_succeeds(self, client, authenticate_user,
                                              new_products, create_user):
        """Should succeed when soft deleting a product"""

        products = new_products
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.product_url(products[0].id, 'soft'),
                                 **auth_header)
        deleted_product = Product.objects.filter(id=products[0].id).first()
        resp = response.data

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['DELETED'].format('Product')
        assert deleted_product.deleted

    def test_deleting_a_product_from_another_vendor_fails(self, client,
                                                          authenticate_user,
                                                          new_products,
                                                          verified_business_user):
        """Should fail when another business owner tries to delete a product"""

        verified_business_user(USER)
        products = new_products
        auth_header = self.authenticate_user(authenticate_user, USER)

        response = client.delete(self.product_url(products[0].id, 'soft'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_deleting_already_soft_deleted_product_fails(self, client,
                                                         create_user,
                                                         authenticate_user,
                                                         new_products):
        """Test that deleting an already deleted product fails"""

        products = new_products
        products[0].deleted = True
        products[0].save()
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.product_url(products[0].id, 'soft'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_restore_a_nonexistent_product_fails(self, client,
                                                 verified_business_user,
                                                 authenticate_user,
                                                 ):
        """Test that restoring an invalid product fails"""

        verified_business_user(NEW_USER)
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(self.product_url('invalid', 'restore'),
                              **auth_header)
        resp = response.data

        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_DELETED']

    def test_that_only_superusers_can_restore_deleted_products_succeeds(self,
                                                                        client,
                                                                        create_superuser,
                                                                        authenticate_user,
                                                                        new_products,
                                                                        ):
        """test that only superusers can restore deleted products"""

        products = new_products
        products[0].deleted = True
        products[0].save()
        create_superuser(USER)
        auth_header = self.authenticate_user(authenticate_user, USER)
        response = client.get(self.product_url(products[0].id, 'restore'),
                              **auth_header)
        resp = response.data

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['RESTORE'].format('Product',
                                                             products[0].title)

    def test_that_vendor_owners_cant_restore_deleted_products_fail(self,
                                                                   client,
                                                                   verified_business_user,
                                                                   authenticate_user,
                                                                   new_products,
                                                                   ):
        """test that vendor owners cannot restore deleted products"""

        products = new_products
        products[0].deleted = True
        products[0].save()
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.get(self.product_url(products[0].id, 'restore'),
                              **auth_header)
        resp = response.data

        assert response.status_code == 400
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_DELETED']

    def test_hard_deleting_a_product_succeeds(self, client, create_user,
                                              authenticate_user,
                                              new_products):
        """Test that hard deleting a product succeeds"""

        products = new_products
        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.product_url(products[0].id, 'hard'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 200
        assert resp['status'] == 'success'
        assert resp['message'] == MESSAGES['P_DELETED'].format('Product')

    def test_hard_deleting_a_nonexistent_vendor_fails(self, client, create_user,
                                                      authenticate_user,
                                                      new_products):
        """Test that hard deleting an invalid product fails"""

        auth_header = self.authenticate_user(authenticate_user, NEW_USER)
        response = client.delete(self.product_url('invalid', 'hard'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_that_superusers_cannot_soft_delete_products_fails(self,
                                                               client,
                                                               create_superuser,
                                                               authenticate_user,
                                                               new_products,
                                                               ):
        """test that only superusers can restore deleted products"""

        products = new_products
        create_superuser(USER)
        auth_header = self.authenticate_user(authenticate_user, USER)
        response = client.delete(self.product_url(products[0].id, 'soft'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']

    def test_that_superusers_cannot_hard_delete_products_fails(self,
                                                               client,
                                                               create_superuser,
                                                               authenticate_user,
                                                               new_products,
                                                               ):
        """test that only superusers can restore deleted products"""

        products = new_products
        create_superuser(USER)
        auth_header = self.authenticate_user(authenticate_user, USER)
        response = client.delete(self.product_url(products[0].id, 'hard'),
                                 **auth_header)
        resp = response.data

        assert response.status_code == 404
        assert resp['status'] == 'error'
        assert resp['message'] == MESSAGES['NOT_FOUND']
