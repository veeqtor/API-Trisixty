"""Test for the home view"""


def test_home_rendered(client):
    """Test the home route"""

    response = client.get('')
    assert response.status_code == 200
