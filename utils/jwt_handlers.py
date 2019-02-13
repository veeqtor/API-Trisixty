"""Module for jwt handling"""
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


def jwt_get_secret_from_user(user):
    """Gets the secret key from the user details"""
    return user.id + '-' + user.email


def jwt_payload_handler(user):
    """JWT payload handler"""
    user_id = user.pop('id')
    payload = {
        'user_id': user_id,
        'user_data': user,
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
        "message": "User successfully logged in",
        'data': {
            'token': token,
        }
    }
