from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from utils.messages import MESSAGES
from utils.validations import password_validation

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta class"""

        model = get_user_model()
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name',  'account_type', 'is_staff',
                  'is_superuser']
        read_only_fields = ['full_name', 'id', 'account_type',
                            'date_joined', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'verification_token': {
                'write_only': True
            },
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def validate_password(self, attrs):
        """Validates the password"""

        password_validation(attrs)
        return attrs

    def create(self, validated_data):
        """create a new user"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Edit the user object"""

        password = validated_data.pop('password')
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(JSONWebTokenSerializer):
    """JWT Token Payload serializer"""

    def validate(self, attrs):
        """Validate and authenticate the user"""
        credentials = {
            'username': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(
            request=self.context.get('request'),
            **credentials
        )
        if user:
            serializer = UserSerializer(user)
            payload = jwt_payload_handler(serializer.data)
            return {
                'token': jwt_encode_handler(payload),
            }

        else:
            raise serializers.ValidationError(
                MESSAGES['UNAUTHENTICATED'], code='authentication')
