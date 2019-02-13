from .serializers import UserSerializer, AuthTokenSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from rest_framework.response import Response

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegister(generics.CreateAPIView):
    """Views for listing all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            payload = jwt_payload_handler(serializer.data)
            token = jwt_encode_handler(payload)
            res = {
                'status': 'success',
                'message': 'You have successfully registered ,'
                'Kindly check your mail to verify your account',
                'data': {
                    'token': token,
                }
            }
            return Response(res, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(ObtainJSONWebToken):
    serializer_class = AuthTokenSerializer
