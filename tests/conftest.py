"""Module for pytest configs"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from vendor.models import Vendor
from product.models import Product

from tests.mocks.user_mock_data import USER, NEW_USER
from tests.mocks.vendor_mock_data import NEW_VENDOR
from tests.mocks.product_mock_data import NEW_PRODUCT

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
def verified_business_user():
    """Fixture to create a user"""

    def verified_user(data):
        user = get_user_model().objects.create_user(**data)
        user.is_verified = True
        user.account_type = 'BUSINESS'
        user.save()
        return user

    return verified_user


@pytest.fixture(scope='function')
def create_product(create_vendor):
    """Fixture to create a new vendor"""

    vendor, user = create_vendor

    NEW_PRODUCT['vendor'] = vendor
    return Product.objects.create(**NEW_PRODUCT), user


@pytest.fixture(scope='function')
def create_vendor(create_user):
    """Fixture to create a user"""
    user = create_user(USER)
    NEW_VENDOR['owner'] = user
    return Vendor.objects.create(**NEW_VENDOR), user


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


@pytest.fixture(scope='function')
def authenticate_user(client):
    def token(user):
        response = client.post(LOGIN_URL, data={
            'email': user['email'],
            'password': user['password']
        }).data
        return response['data']['token']

    return token


@pytest.fixture(scope='function')
def new_vendors(verified_business_user):
    """To create vendors"""

    user = verified_business_user(NEW_USER)

    data = [
        {

            "name": "Business",
            "location": "Unknown Location",
            "description": "New description",
            "logo_url": "https://place-hold.it/300x500/fff",
            "owner": user,
            "email": "new_vendor@example.com",
            "phone": "07068662986"

        }, {

            "name": "BusinessI",
            "location": "Unknown Location",
            "description": "New description",
            "logo_url": "https://place-hold.it/300x500/fff",
            "owner": user,
            "email": "new_vendorI@example.com",
            "phone": "07068662986"

        }, {

            "name": "BusinessII",
            "location": "Unknown Location",
            "description": "New description",
            "logo_url": "https://place-hold.it/300x500/fff",
            "owner": user,
            "email": "new_vendorII@example.com",
            "phone": "07068662986"

        }, {

            "name": "BusinessIII",
            "location": "Unknown Location",
            "description": "New description",
            "logo_url": "https://place-hold.it/300x500/fff",
            "owner": user,
            "email": "new_vendorIII@example.com",
            "phone": "07068662986"
        },
    ]

    return [Vendor.objects.create(**d) for d in data]


@pytest.fixture(scope='function')
def new_products(new_vendors):
    """To create products"""

    vendor = new_vendors

    data = [
        {
            "title": "Leggings I",
            "price": 23.23,
            "description": "New description",
            "images": ["https://place-hold.it/300x500/fff",
                       "https://place-hold.it/300x500/fff"],
            "vendor": vendor[0]
        }, {

            "title": "Trouser II",
            "price": 23.23,
            "description": "New description",
            "images": ["https://place-hold.it/300x500/fff",
                       "https://place-hold.it/300x500/fff"],
            "vendor": vendor[1]
        }, {

            "title": "Short III",
            "price": 23.23,
            "description": "New description",
            "images": ["https://place-hold.it/300x500/fff",
                       "https://place-hold.it/300x500/fff"],
            "vendor": vendor[2]
        }, {

            "title": "Gown IV",
            "price": 23.23,
            "description": "New description",
            "images": ["https://place-hold.it/300x500/fff",
                       "https://place-hold.it/300x500/fff"],
            "vendor": vendor[3]
        }, {

            "title": "Shirt V",
            "price": 23.23,
            "description": "New description",
            "images": ["https://place-hold.it/300x500/fff",
                       "https://place-hold.it/300x500/fff"],
            "vendor": vendor[0]
        }
    ]

    return [Product.objects.create(**d) for d in data]
