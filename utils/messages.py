"""Module for messages"""

MESSAGES = {
    'NO_PERMISSION': {
        'status': 'error',
        'errors': 'You don\'t have permission to perform this action.'
    },
    'FETCHED':
        '{} successfully fetched.',
    'DUPLICATES':
        '{} with this {} already exists.',
    'CREATED':
        '{} successfully created.',
    'REGISTER':
        'You have successfully registered, please check '
        'your email to verify your account.',
    'LOGIN':
        'You have successfully logged in.',
    'UNAUTHENTICATED':
        'Unable to authenticate with provided credentials, '
        'Please enter the correct Email and password.',
    'ERROR':
        'An error occurred',
    'REQUIRED_FIELD':
        'This field is required.',
    'BLANK_FIELD': 'This field may not be blank.',
    'NOT_FOUND':
        'Oops!, Sorry we could not find you on our system.',
    'EMAIL_FORMAT':
        'You have entered an invalid email.',
    'INVALID_PASSWORD':
        'Password must be alphanumeric and must contain at least one special character.',
    'NOT_VERIFIED':
        'You need to verify your account',
    'EXPIRED_TOKEN':
        'Unfortunately, this token has expired or is invalid',
    'ALREADY_VERIFIED': 'Your account has already been verified.',
    'VERIFIED': 'You have successfully verified your account.',
    'RESEND_TOKEN':
        'You have successfully resent your verification token.',
    'INVALID_TOKEN': 'Please provide a valid token.',
    'INVALID_EMAIL':
        'You have provided an invalid email',
    'NOT_FOUND_TOKEN':
        'Sorry, the token provided is not attached to any user or is invalid.',
    'PASSWORD_RESET': 'A password reset token has been sent to your email.',
    'PASSWORD_RESET_SUCCESS': 'Your password reset was successful.',
    'RESET_LINK':
        'A reset link have been sent to your email.',
    'UNREGISTER_USER': 'Unfortunately, this is not a registered user.'
}
