"""Custom error handler module"""

from rest_framework import status
from rest_framework.views import exception_handler
from utils.messages import MESSAGES


def custom_exception_handler(exc, context):
    """Custom exception handler"""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            'status': 'error',
            'message': MESSAGES['NOT_FOUND']
        }

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        response.data = {
            'status': 'error',
            'message': MESSAGES['ERROR']
        }

    return response

