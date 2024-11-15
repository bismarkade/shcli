import pytest
from unittest.mock import patch

from shcli.auth.login_model import LoginModel
from shcli.auth.user_auth import LoginAuth

@patch("requests_oauthlib.OAuth2Session.fetch_token")
def test_get_token(mock_fetch_token):
    """
    Test token generation logic.
    """
    mock_fetch_token.return_value = {"access_token": "fake_token"}
    login_model = LoginModel(client_id="test_id", client_secret="test_secret")
    auth = LoginAuth(login_model)
    token = auth.get_token()
    assert token["access_token"] == "fake_token"
