import pytest
from unittest.mock import patch

from shcli.catalog.catalog import catalog_request, extract_statistics

@patch("requests.post")
def test_catalog_request(mock_post):
    """
    Test catalog request logic.
    """
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"features": []}
    
    token = "token"
    bbox = [12.0, 47.0, 13.0, 48.0]
    response = catalog_request(token, ["collection"], "2022-10-01T00:00:00Z/2024-10-01T23:59:59Z", bbox)
    
    mock_post.assert_called_once()
    assert response == {"features": []}

def test_extract_statistics():
    """
    Test catalog statistics extraction logic.
    """
    response = {
        "features": [
            {"id": "1", "properties": {"datetime": "2023-01-01", "eo:cloud_cover": 10}},
            {"id": "2", "properties": {"datetime": "2023-01-02", "eo:cloud_cover": 20}}
        ]
    }
    stats = extract_statistics(response)
    assert len(stats) == 2
    assert stats[0]["id"] == "1"
