import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from tests.mocks.user_mock_data import USER


REGISTER_URL = reverse('user:register')
LOGIN_URL = reverse('user:login')
VERIFY_URL = reverse('user:verify')
RESEND_TOKEN = reverse('user:resend_token')


@pytest.fixture(scope='function')
def create_user():
    """Fixture to create a user"""
    def user(data):
        return get_user_model().objects.create_user(**data)
    return user


@pytest.fixture(scope='function')
def create_superuser():
    """Fixture to create a user"""
    def super_user(data):
        return get_user_model().objects.create_superuser(**data)
    return super_user


@pytest.fixture(scope='function')
def generate_token(client, create_user):
    """Fixture to generate token by user"""
    def generate_token(user):
        create_user(user)
        response = client.post(LOGIN_URL, data={
            'email': user['email'],
            'password': user['password']
        }).data
        return response['data']['token']
    return generate_token


@pytest.fixture(scope='function')
def create_user_and_token(client):
    """Fixture to generate a user token."""

    client.post(REGISTER_URL, data={**USER})
    user = get_user_model().objects.all().filter(
        email=USER['email']).first()
    return user


@pytest.fixture(scope='function')
def verify_token(client, create_user_and_token):
    """Fixture to generate a user token."""

    verification_token = create_user_and_token.verification_token
    client.get(VERIFY_URL + f'?token={verification_token}')

    return create_user_and_token


@pytest.fixture(scope='function')
def auth_header(client, generate_token):
    """Authentication header"""

    token = generate_token(USER)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {token}'
    }
