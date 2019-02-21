"""API View module for users"""

from .serializers import UserSerializer, AuthTokenSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, views
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from rest_framework.response import Response
from utils import random_token, messages
from tasks.user_emails import UserSend


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegister(generics.CreateAPIView):
    """Class representing the view for creating a user"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Creates a new user
        Args:
            request (object): Request object
            *args:
            **kwargs:

        Returns:
            JSON

        """
        serializer = UserSerializer(data=request.data)
        random_number = random_token.generate_verification_token(10)
        if serializer.is_valid():
            serializer.validated_data['verification_token'] = random_number
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            payload = jwt_payload_handler(serializer.data)
            token = jwt_encode_handler(payload)
            res = {
                'status': 'success',
                'message': messages.MESSAGES['REGISTER'],
                'data': {
                    'token': token,
                }
            }
            return Response(res, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(ObtainJSONWebToken):
    """Class representing the Login view"""

    serializer_class = AuthTokenSerializer


class UserAccountVerification(views.APIView):
    """Class representing the endpoint to verify the user account"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        """

        Args:
            request (object): Request object
            *args:
            **kwargs:

        Returns:
            JSON

        """

        token = request.query_params.get('token')

        if not token:
            return Response({
                'status': 'error',
                'message': messages.MESSAGES['INVALID_TOKEN']
            }, status=status.HTTP_400_BAD_REQUEST)

        found_token = self.queryset.filter(verification_token=token).first()

        if not found_token:
            return Response({
                'status': 'error',
                'message': messages.MESSAGES['NOT_FOUND_TOKEN']
            }, status=status.HTTP_404_NOT_FOUND)

        if not found_token.is_verified and random_token.is_valid(token):
            found_token.verification_token = None
            found_token.is_verified = True
            found_token.save()
            msg = {
                'status': 'success',
                'message': messages.MESSAGES['VERIFIED']
            }
            return Response(msg, status=status.HTTP_200_OK)

        msg = {
            'status': 'error',
            'message': messages.MESSAGES['EXPIRED_TOKEN']
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class UserVerificationTokenResend(views.APIView):
    """Class representing the endpoint to
    resend the account verification token"""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        """Get method for the verification route"""

        random_number = random_token.generate_verification_token(10)
        user = request.user
        if user.is_verified:
            msg = {
                'status': 'error',
                'message': messages.MESSAGES['ALREADY_VERIFIED']
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
        user.verification_token = random_number
        user.save()
        UserSend.verification_email(user.id)
        msg = {
            'status': 'success',
            'message': messages.MESSAGES['RESEND_TOKEN']
        }
        return Response(msg, status=status.HTTP_200_OK)


class UserPasswordReset(views.APIView):
    """Class representing the endpoints for user's password reset"""

    serializer_class = UserSerializer

    def post(self, request):
        """Post method to send out password reset email"""

        email = request.data.get('email')
        user = get_user_model().objects.filter(email=email).first()
        random_number = random_token.generate_verification_token(10)

        if not user:
            msg = {
                'status': 'error',
                'message': messages.MESSAGES['UNREGISTER_USER']
            }
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        user.password_reset = random_number
        user.save()
        UserSend.password_reset_email(user.id)
        msg = {
            'status': 'success',
            'message': messages.MESSAGES['PASSWORD_RESET']
        }
        return Response(msg, status=status.HTTP_200_OK)

    def patch(self, request):
        """Patch method to reset password"""

        token = request.query_params.get('token')
        user = get_user_model().objects.filter(password_reset=token).first()

        if token and not random_token.is_valid(token):
            msg = {
                'status': 'error',
                'message': messages.MESSAGES['EXPIRED_TOKEN']
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            save_user = serializer.save()
            save_user.password_reset = None
            save_user.save()

            msg = {
                'status': 'success',
                'message': messages.MESSAGES['PASSWORD_RESET_SUCCESS']
            }
            return Response(msg, status=status.HTTP_200_OK)

        msg = {
            'status': 'error',
            'message': messages.MESSAGES['NOT_FOUND_TOKEN']
        }
        return Response(msg, status=status.HTTP_404_NOT_FOUND)
