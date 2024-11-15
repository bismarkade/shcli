import os
from shapely.geometry import box
from typing import Dict, List, Optional

import json
import logging

from auth.login_model import LoginModel



logger = logging.getLogger(__name__)

def validate_bbox(bbox: Optional[List[float]]) -> bool:
    """
    Validates the bounding box coordinates using Shapely.

    Args:
        bbox: Bounding box coordinates [minLon, minLat, maxLon, maxLat].

    """
    if bbox is None:
        logger.info("No bounding box provided.")
        return False

    if len(bbox) != 4 or bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
        logger.error("Invalid bounding box.")
        return False

    try:
        if box(*bbox).is_valid:
            logger.info("Bounding box validated successfully.")
            return True
    except Exception as e:
        logger.error(f"Bounding box validation error: {e}")

    return False


def save_login_credentials(
                        client_id: str, 
                        client_secret: str, 
                        file_path: str = "auth_credentials.json"
                    ) -> None:
    """
    Saves login credentials securely to a file.
   
    """
    credentials = {
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        with open(file_path, "w") as file:
            json.dump(credentials, file)
        logger.info("Credentials saved securely.")
    except Exception as e:
        logger.error(f"Error saving credentials: {e}")



def read_login_credentials(file_path: str = "auth_credentials.json") -> Dict[str, str]:
    """
    Reads login credentials from a file.
    Args:
        file_path (str): Path to the credentials file. Default is "auth_credentials.json".

    """
    try:
        logger.info(f"Attempting to read credentials from {file_path}...")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found. Please authenticate first.")

        with open(file_path, "r") as file:
            credentials = json.load(file)

            login_credentials = LoginModel(client_id=credentials['client_id'], client_secret=credentials['client_secret'])
            logger.info("Credentials loaded successfully.")

            return login_credentials
    except FileNotFoundError:
        logger.error(f"{file_path} not found. Please authenticate first.")
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error reading credentials: {e}")
        raise
