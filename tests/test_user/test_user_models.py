import pytest
from tests.mocks.user_mock_data import USER, SUPERUSER, USER_INVALID
pytestmark = pytest.mark.django_db


class TestUserModel:
    """Test user model"""

    def test_user_creation(self, create_user):
        """Test that a user can be successfully created"""

        user = create_user(USER)
        assert user.email == USER['email']
        assert user.first_name == USER['first_name']
        assert user.last_name == USER['last_name']
        assert user.full_name == f'{user.first_name} {user.last_name}'
        assert user.check_password(USER['password'])

    def test_super_user_creation(self, create_superuser):
        """Test that a super user is created"""
        super_user = create_superuser(SUPERUSER)
        assert super_user.email == SUPERUSER['email']
        assert super_user.check_password(SUPERUSER['password'])
        assert super_user.is_superuser
        assert super_user.is_staff

    def test_create_user_with_no_email(self, create_user):
        """Test user creation with no email"""
        with pytest.raises(ValueError):
            create_user(USER_INVALID)
