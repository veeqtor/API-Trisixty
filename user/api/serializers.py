from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    created_at = serializers.DateTimeField(
        default=serializers.CreateOnlyDefault(timezone.now)
    )

    class Meta:
        model = get_user_model()
        fields = '__all__'
        # fields = ['email', 'password',
        #           'account_type', 'first_name', 'last_name']
        read_only_fields = ['full_name', 'id', 'date_joined']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

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


class TokenPayloadSerializer(serializers.ModelSerializer):
    """JWT Token Payload serializer"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'last_login', 'date_joined',
                  'account_type', 'first_name', 'last_name', 'is_staff',
                  'is_superuser')
        read_only_fields = ('full_name', 'id', 'date_joined')
