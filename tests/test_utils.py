import os
import json
import pytest
from shcli.utils.utils import read_login_credentials, save_login_credentials, validate_bbox

@pytest.fixture(scope="function")
def temp_credentials_file(tmp_path):
    """
    Create a temporary credentials file for tests.
    """
    file_path = tmp_path / "auth_credentials.json"
    with open(file_path, "w") as file:
        file.write('{"client_id": "test_id", "client_secret": "test_secret"}')
    return file_path

@pytest.mark.parametrize(
    "bbox, expected",
    [
        ([12.0, 47.0, 13.0, 48.0], True),
        ([13.0, 48.0, 12.0, 47.0], False),
        ([], False),
        (None, False),
    ]
)

def test_validate_bbox(bbox, expected):
    """
    Test bounding box validation utility.
    """
    assert validate_bbox(bbox) == expected

def test_save_login_credentials(tmp_path):
    """
    Test saving login credentials.
    """
    file_path = tmp_path / "auth_credentials.json"
    save_login_credentials("test_client_id", "test_client_secret", str(file_path))
    assert os.path.exists(file_path)
    with open(file_path, "r") as file:
        credentials = json.load(file)
        assert credentials["client_id"] == "test_client_id"
        assert credentials["client_secret"] == "test_client_secret"


def test_read_login_credentials(temp_credentials_file):
    """
    Test reading login credentials.
    """
    credentials = read_login_credentials(str(temp_credentials_file))
    assert credentials.client_id == "test_id"  
    assert credentials.client_secret == "test_secret"

def test_read_login_credentials_file_not_found():
    """
    Test behavior when credentials file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        read_login_credentials("non_existent_file.json")
