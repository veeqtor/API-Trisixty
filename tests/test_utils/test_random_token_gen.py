from utils.random_token import generate_verification_token, is_valid


class TestRandomTokenGenerator:
    """Tests the random token generator"""

    def test_token_generation_succeeds(self):
        """Tests that a random token was generated"""

        token = generate_verification_token(5)
        assert token

    def test_verify_token_succeeds(self):
        """Test that the verify token method works"""

        token = generate_verification_token(1)
        assert is_valid(token)

    def test_verify_token_fails(self):
        """Test that a token has expired"""

        token = generate_verification_token(-2)
        assert is_valid(token) is False
