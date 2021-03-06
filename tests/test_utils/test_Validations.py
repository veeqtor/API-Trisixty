import pytest
from utils.validations import email_validation, serializers, password_validation


class TestValidations:
    """class to test the validations utils"""

    def test_email_validations_fails(self):
        """Test the email validations"""
        email = 'test_userexample.com'

        with pytest.raises(serializers.ValidationError) as excinfo:
            email_validation(email)

    def test_password_validations_fails(self):
        """Test the password validations"""
        password = "password@#"

        with pytest.raises(serializers.ValidationError) as excinfo:
            password_validation(password)
