import secrets
import binascii
from datetime import datetime, timedelta


def generate_verification_token(exp=5):
    """
    Generates the verification token
    Args:
        exp {int}: The expiration time in minutes

    Returns:
        str - Token string

    """
    rand = secrets.token_urlsafe(16)
    rand_ii = secrets.token_urlsafe(16)
    date = datetime.now() + timedelta(minutes=exp)
    date_timestamp = str(round(date.timestamp())).encode('ascii')
    encoded_timestamp = binascii.hexlify(date_timestamp).decode('ascii')
    token = rand + '-' + encoded_timestamp + '_-' + rand_ii

    return token


def is_valid(token):
    """
    Checks if the token is valid.

    Args:
        token {str}: Token

    Returns:
        Boolean - True or false

    """
    now = datetime.now().timestamp()
    time = token[23:][:20]
    decode_timstamp = binascii.unhexlify(time).decode('ascii')
    if now > int(decode_timstamp):
        return False
    else:
        return True
