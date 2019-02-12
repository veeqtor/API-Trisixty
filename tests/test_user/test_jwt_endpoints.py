import pytest
from django.urls import resolve, reverse
from tests.mocks.user_mock_data import USER

TOKEN_URL = reverse('token')
TOKEN_REFRESH = reverse('token_refresh')
TOKEN_VERIFY = reverse('token_verify')


class TestUserJWTUrls:
    """Class to test out the jwt routes"""

    def test_jwt_paths_url_succeeds(self):
        """Test the JWT authentication paths"""
        assert resolve(TOKEN_URL).view_name == 'token'
        assert resolve(TOKEN_REFRESH).view_name == 'token_refresh'
        assert resolve(TOKEN_VERIFY).view_name == 'token_verify'

    @pytest.mark.django_db
    def test_jwt_token_generation(self, client, create_user):
        """Test that a JWT token is generated"""

        create_user(USER)
        response = client.post(TOKEN_URL, data={
            'email': USER['email'],
            'password': USER['password']
        })
        resp_data = response.data

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['data']['token'] is not None

    @pytest.mark.django_db
    def test_jwt_token_verify_succeeds(self, client, generate_token):
        """Test that a JWT token is verification"""

        token = generate_token(USER)
        response = client.post(TOKEN_VERIFY, data={
            'token': token,
        })
        resp_data = response.data

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['data']['token'] is not None

    @pytest.mark.django_db
    def test_jwt_token_refresh_succeeds(self, client, generate_token):
        """Test that a JWT token is verification"""

        token = generate_token(USER)
        response = client.post(TOKEN_REFRESH, data={
            'token': token,
        })
        resp_data = response.data

        assert response.status_code == 200
        assert resp_data['status'] == 'success'
        assert resp_data['data']['token'] is not None

    @pytest.mark.django_db
    def test_jwt_token_verify_fails(self, client, generate_token):
        """Test that a JWT token is verification"""
        response = client.post(TOKEN_VERIFY, data={
            'token': 'token',
        })
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_jwt_token_refresh_fails(self, client):
        """Test that a JWT token is verification"""

        response = client.post(TOKEN_REFRESH, data={
            'token': 'token',
        })
        assert response.status_code == 400
