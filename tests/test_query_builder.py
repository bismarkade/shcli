import pytest
from shcli.process.query_builder import create_request_data

def test_create_request_data():
    """
    Test query builder for creating request data.
    """
    bbox = [12.0, 47.0, 13.0, 48.0]
    data = create_request_data(bbox, "2022-01-01", "2022-12-31", 20, "leastCC", "sentinel-2-l2a", "NDVI")
    assert "input" in data
    assert "output" in data
    assert data["input"]["data"][0]["dataFilter"]["maxCloudCoverage"] == 20
