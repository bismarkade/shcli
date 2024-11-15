import requests
from typing import Any, Dict
import logging

from utils.file_utils import save_image_to_file

logger = logging.getLogger(__name__)

def process_request(
    token: str,
    data: Dict[str, Any],
    url: str = "https://services.sentinel-hub.com/api/v1/process",
    output_file: str = "output_image.jpg"
) -> None:
    """
    Makes a Sentinel Hub Process API request and handles image responses.

    Args:
        token (str): Bearer token for authentication.
        data (dict): The request payload for the Sentinel Hub Process API.
        url (str): The API endpoint URL (default: Sentinel Hub Process API endpoint).
        output_file (str): Filepath to save the returned image.

    Returns:
        None: The image is saved to the specified file.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        logger.info(f"Sending POST request to {url} with provided data.")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        
        logger.info("Request successful. Saving the image to the specified file.")
        save_image_to_file(response.content, output_file)

    except requests.RequestException as e:
        logger.error("Error making the API request:", e)
