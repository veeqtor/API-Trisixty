import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


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
        response = client.post(reverse('token'), data={
            'email': user['email'],
            'password': user['password']
        }).data
        return response['data']['token']
    return generate_token
