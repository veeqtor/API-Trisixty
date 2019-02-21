import pytest
from django.urls import resolve, reverse
from django.core import mail
from django.contrib.auth import get_user_model
from tests.mocks.user_mock_data import USER
from utils.messages import MESSAGES
from utils.random_token import generate_verification_token

RESET_PASSWORD = reverse('user:reset_password')


@pytest.mark.django_db
class TestUserPasswordResetEndpoints:
    """Class to test out the user password reset routes"""

    def test_password_reset_url_succeeds(self):
        """Test that the urls are accessible"""
        assert resolve(RESET_PASSWORD).view_name == 'user:reset_password'

    def test_sending_password_reset_token_succeeds(self, create_user, client):
        """Test that the password token email is sent"""
        create_user(USER)

        response = client.post(RESET_PASSWORD, data={
            'email': USER['email']
        })

        resp = response.data
        email = mail.outbox[1]

        assert response.status_code == 200
        assert len(mail.outbox) == 2
        assert email.subject == 'Password Reset'
        assert 'status' in resp
        assert resp['message'] == MESSAGES['PASSWORD_RESET']

    def test_sending_password_reset_token_fails(self, client):
        """Test that the email is a valid and registered email"""

        response = client.post(RESET_PASSWORD, data={
            'email': USER['email']
        })

        resp = response.data

        assert response.status_code == 404
        assert 'status' in resp
        assert resp['message'] == MESSAGES['UNREGISTER_USER']

    def test_password_reset_token_fails(self, client):
        """Test for when an invalid token is passed"""

        token = generate_verification_token(-5)

        response = client.patch(RESET_PASSWORD + f'?token={token}', data={
            'password': USER['email']
        })

        resp = response.data

        assert response.status_code == 400
        assert 'status' and 'message' in resp
        assert resp['message'] == MESSAGES['EXPIRED_TOKEN']

    def test_password_reset_with_invalid_token_succeeds(self, client,
                                                        create_user):
        """Test for when an expired token is provided"""

        create_user(USER)
        token = generate_verification_token(5)

        user = get_user_model().objects.filter(email=USER['email']).first()
        user.password_reset = token
        user.save()

        response = client.patch(RESET_PASSWORD + f'?token={token}',
                                content_type='application/json',
                                data={'password': USER['password']}
                                )

        resp = response.data

        assert response.status_code == 200
        assert 'status' and 'message' in resp
        assert resp['message'] == MESSAGES['PASSWORD_RESET_SUCCESS']

    def test_password_reset_with_invalid_token_fails(self, client, create_user):
        """Test for when an expired token is provided"""

        create_user(USER)
        token = generate_verification_token(5)

        user = get_user_model().objects.filter(email=USER['email']).first()
        user.password_reset = None
        user.save()

        response = client.patch(RESET_PASSWORD + f'?token={token}',
                                content_type='application/json',
                                data={'password': USER['password']}
                                )

        resp = response.data

        assert response.status_code == 404
        assert 'status' and 'message' in resp
        assert resp['message'] == MESSAGES['NOT_FOUND_TOKEN']

    def test_password_reset_invalid_password(self, client, create_user):
        """Test an invalid password"""

        create_user(USER)
        token = generate_verification_token(5)

        user = get_user_model().objects.filter(email=USER['email']).first()
        user.password_reset = token
        user.save()

        response = client.patch(RESET_PASSWORD + f'?token={token}',
                                content_type='application/json',
                                data={'password': USER['email']}
                                )
        resp = response.data

        assert response.status_code == 400
        assert resp['password'][0] == MESSAGES['INVALID_PASSWORD']
