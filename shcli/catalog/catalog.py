import requests
from typing import Any, Dict, List
import logging

from utils.utils import validate_bbox


logger = logging.getLogger(__name__) 

def catalog_request(
    token: str,
    collections: List[str],
    datetime: str,
    bbox: List[float],
    limit: int = 10,
    cloud_cover: int = 20,
    url: str = "https://services.sentinel-hub.com/api/v1/catalog/1.0.0/search"
) -> Dict[str, Any]:
    """
    Sends a request to the Sentinel Hub Catalog API.

    Args:
        token (str): Bearer token for authentication.
        collections (list): List of collections to search.
        datetime (str): Date range for the search (e.g., "2022-10-24T00:00:00Z/2024-10-24T10:17:27Z").
        bbox (list): Bounding box coordinates [minLon, minLat, maxLon, maxLat].
        limit (int): Maximum number of results to return (default: 10).
        cloud_cover (int): Maximum cloud cover percentage (default: 20).
        url (str): The API endpoint URL (default: Sentinel Hub Catalog API endpoint).

    Returns:
        Dict[str, Any]: The API response as a dictionary.
    """
    if not validate_bbox(bbox):
        logger.error("Invalid bounding box provided. Aborting request.")
        return {}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "collections": collections,
        "datetime": datetime,
        "bbox": bbox,
        "limit": limit,
        "filter": {
            "op": "<=",
            "args": [
                {
                    "property": "eo:cloud_cover"
                },
                cloud_cover
            ]
        },
        "filter-lang": "cql2-json"
    }

    try:
        logging.info("Sending request to Sentinel Hub Catalog API.")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        logging.info("Catalog request successful.")
        return response.json()  
    except requests.RequestException as e:
        print("Error making the catalog request:", e)
        return {}


# update docs   
def extract_statistics(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extracts statistics from the Sentinel Hub Catalog API response.

    Args:
        response: The response in a list [id, stac_version, datetime,platform,constellation, 
                    gsd,eo:cloud_cover,proj:epsg ].
    """

    features = response.get("features", [])
    statistics = []

    for feature in features:
        properties = feature.get("properties", {})
        stats = {
            "id": feature.get("id"),
            "stac_version": response.get("stac_version"),
            "datetime": properties.get("datetime"),
            "platform": properties.get("platform"),
            "constellation": properties.get("constellation"),
            "gsd": properties.get("gsd"),
            "eo:cloud_cover": properties.get("eo:cloud_cover"),
            "proj:epsg": properties.get("proj:epsg"),
        }

        statistics.append(stats)

    return statistics
