import pytest
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from tests.mocks.user_mock_data import USER, USER_INVALID
from utils.messages import MESSAGES
from utils.random_token import generate_verification_token


REGISTER_URL = reverse('user:register')
LOGIN_URL = reverse('user:login')
VERIFY_URL = reverse('user:verify')
RESEND_TOKEN = reverse('user:resend_token')


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
        assert resp_data['non_field_errors'][0] == MESSAGES['UNAUTHENTICATED']

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

    def test_user_verify_token_succeeds(self, client, create_user_and_token):
        """Test the route for token verification"""
        verification_token = create_user_and_token.verification_token
        response = client.get(VERIFY_URL + f'?token={verification_token}')
        resp_data = response.data
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['message'] == MESSAGES['VERIFIED']

    def test_user_verification_fails(self, client):
        """Test that verification fails"""
        response = client.get(VERIFY_URL)
        resp_data = response.data
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert resp_data['message'] == 'Please provide a valid token.'

    def test_that_user_is_already_verification_succeeds(self, client,
                                                        verify_token):
        """Test that the user is already verified"""
        token = verify_token.verification_token
        response = client.get(VERIFY_URL + f'?token={token}')
        resp_data = response.data
        assert response.status_code == 404
        assert resp_data['status'] == 'error'
        assert resp_data['message'] == MESSAGES['NOT_FOUND_TOKEN']

    def test_that_user_token_expired_succeeds(self, client):
        """Test that the user is already verified"""

        token = generate_verification_token(-5)
        client.post(REGISTER_URL, data={
            'email': 'test2@example.com',
            'password': 'Password@1342'
        })
        get_user_model().objects.all().filter(
            email='test2@example.com').update(verification_token=token)
        response = client.get(VERIFY_URL + f'?token={token}')
        resp_data = response.data
        assert response.status_code == 400
        assert resp_data['status'] == 'error'
        assert resp_data['message'] == MESSAGES['EXPIRED_TOKEN']

    def test_token_resend_succeeds(self, client, auth_header):
        """Test that the token can be resent."""

        response = client.get(RESEND_TOKEN, **auth_header)
        resp_data = response.data
        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['message'] == MESSAGES['RESEND_TOKEN']

    def test_already_verified_token_resend_fails(self, client, create_user):
        """Test that the token cant be resent."""
        user = create_user(USER)
        get_user_model().objects.all().filter(
            email=user.email).update(is_verified=True)
        token = client.post(LOGIN_URL, data={
            'email': user.email,
            'password': 'Password@1234'
        }).data['data']['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        response = client.get(RESEND_TOKEN, **header)
        resp_data = response.data
        assert response.status_code == 403
        assert resp_data['status'] == 'error'
        assert resp_data['message'] == MESSAGES['ALREADY_VERIFIED']
