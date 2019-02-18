from .serializers import UserSerializer, AuthTokenSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, views
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from rest_framework.response import Response
from utils import random_token, messages
from utils.email_services import EmailConcrete


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

send_email = EmailConcrete().send_email


class UserRegister(generics.CreateAPIView):
    """Views for listing all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Creates a new user
        Args:
            request:
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
            email = serializer.data['email']
            content = f'http://localhost:8000/api/v1/user/verify/?token={random_number}'
            send_email(
                'Activate Account', email, content=content)
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
    """Login view"""

    serializer_class = AuthTokenSerializer


class UserAccountVerification(views.APIView):
    """Endpoint to verify the user account"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        """

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """

        token = request.query_params.get('token')

        if not token:
            return Response({
                'status': 'error',
                'message': messages.MESSAGES['INVALID_TOKEN']
            }, status=status.HTTP_400_BAD_REQUEST)

        found_token = self.queryset.filter(verification_token=token)

        if not found_token:
            return Response({
                'status': 'error',
                'message': messages.MESSAGES['NOT_FOUND_TOKEN']
            }, status=status.HTTP_404_NOT_FOUND)

        if random_token.is_valid(token):
            found_token.update(verification_token=None, is_verified=True)
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
    """Endpoint to resend the account verification token"""

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
        content = f'http://localhost:8000/api/v1/user/verify/?token={random_number}'
        send_email(
            'Resend Verification Token', request.user.email, content=content)
        msg = {
            'status': 'success',
            'message': messages.MESSAGES['RESEND_TOKEN']
        }
        return Response(msg, status=status.HTTP_200_OK)
