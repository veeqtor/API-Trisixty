"""Module for jwt handling"""
from user.api.serializers import TokenPayloadSerializer
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


def jwt_get_secret_from_user(user):
    """Gets the secret key from the user details"""

    user_data = TokenPayloadSerializer(user).data
    return user_data['id'] + '-' + user_data['email']


def jwt_get_email_from_payload_handler(payload):
    """Gets the email from the payload"""
    return payload['user_data'].get('email')


def jwt_payload_handler(user):
    """JWT payload handler"""
    user_data = TokenPayloadSerializer(user).data
    user_data.pop('id')
    payload = {
        'user_id': user.pk,
        'user_data': user_data,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    """Returns the response data for both the login and refresh views."""

    return {
        'status': 'success',
        'data': {
            'token': token,
        }
    }
