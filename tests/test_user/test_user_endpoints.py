import pytest
from django.urls import resolve, reverse
from rest_framework.exceptions import ErrorDetail
from tests.mocks.user_mock_data import USER, USER_INVALID
from utils.messages import MESSAGES


REGISTER_URL = reverse('user:register')
LOGIN_URL = reverse('user:login')


@pytest.mark.django_db
class TestUserEndpoints:
    """Class to test out the jwt routes"""

    def test_user_url_succeeds(self):
        """Test the JWT authentication paths"""
        assert resolve(REGISTER_URL).view_name == 'user:register'
        assert resolve(LOGIN_URL).view_name == 'user:login'

    def test_user_login_succeeds(self, client, create_user):
        """Test that a JWT token is generated"""

        create_user(USER)
        response = client.post(LOGIN_URL, data={
            'email': USER['email'],
            'password': USER['password']
        })
        resp_data = response.data

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['data']['token'] is not None

    def test_user_login_fails(self, client, create_user):
        """Test that a JWT token is generated"""
        create_user(USER)
        response = client.post(LOGIN_URL, data={
            'email': '',
            'password': ''
        })
        resp_data = response.data
        assert response.status_code == 400
        assert resp_data['email'][0] == MESSAGES['BLANK_FIELD']
        assert resp_data['password'][0] == MESSAGES['BLANK_FIELD']

    def test_user_login_authentication_fails(self, client, create_user):
        """Test that a JWT token is generated"""
        response = client.post(LOGIN_URL, data={
            'email': 'test1@example1.com',
            'password': 'Password@1234'
        })
        resp_data = response.data
        assert response.status_code == 400
        resp_data['non_field_errors'] == MESSAGES['UNAUTHENTICATED']

    def test_user_account_registration_succeeds(self, client):
        """Test that users can register"""

        response = client.post(REGISTER_URL, data={**USER})
        resp_data = response.data
        assert response.status_code == 201
        assert resp_data['status'] == 'success'
        assert resp_data['data']['token'] is not None

    def test_user_account_registration_fails(self, client):
        """Test that users can register"""

        response = client.post(REGISTER_URL, data={})
        resp_data = response.data
        assert response.status_code == 400
        assert resp_data['email'][0] == MESSAGES['REQUIRED_FIELD']
        assert resp_data['password'][0] == MESSAGES['REQUIRED_FIELD']

    def test_user_account_registration_invalid_details_fails(self, client):
        """Test that users can register"""

        response = client.post(REGISTER_URL, data={**USER_INVALID})
        resp_data = response.data
        assert response.status_code == 400
        assert resp_data['email'][0] == MESSAGES['BLANK_FIELD']
        assert resp_data['password'][0] == MESSAGES['INVALID_PASSWORD']
