from typing import List, Optional
import click
import json

import logging

from shcli.auth.login_model import LoginModel
from shcli.auth.user_auth import LoginAuth
from shcli.catalog.catalog import catalog_request, extract_statistics
from shcli.process.process import process_request
from shcli.process.query_builder import create_request_data
from shcli.utils.utils import read_login_credentials, save_login_credentials, validate_bbox



logger = logging.getLogger(__name__)

@click.group()
def cli():
    """shcli is a CLI Tool for interacting with Sentinel Hub API."""
    # logging.getLogger().setLevel(logging.DEBUG)
    pass

@cli.command(name="example")
def show_examples():
    """
    Example commands for using shcli.
    """
    examples = """
    Example Usage:
    
    1. Authenticate:
       shcli auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

    2. Get Images:
        - NDVI
        shcli getimages --bbox 12.845434 47.753636 13.099575 47.882276 --start-date 2022-10-01 --end-date 2024-10-31 --satellite-type sentinel-2-l2a --output-type NDVI --output-format PNG --output-file output_image
        
        - VISUAL 
        shcli getimages --bbox 12.845434 47.753636 13.099575 47.882276 --start-date 2022-10-01 --end-date 2024-10-31 --satellite-type sentinel-2-l2a --output-type VISUAL --output-format PNG --output-file VISUAL_image
   
     3. Generate Catalog Statistics:
       shcli catalog-s --bbox 12.845434 47.753636 13.099575 47.882276 --start-date 2022-10-01 --end-date 2024-10-31
    """
    click.echo(examples)


@cli.command()
@click.option("--client-id", prompt=True, help="Sentinel Hub Client ID.")
@click.option("--client-secret", prompt=True, hide_input=True, help="Sentinel Hub Client Secret.")
def auth(client_id: str, client_secret: str):
    """
    Authenticate and securely save credentials.
    """
    try:
        logger.info("Authenticating...")
        login_credentials = LoginModel(client_id=client_id, client_secret=client_secret)
        token = LoginAuth(login_credentials).get_token()

        logger.info("Authentication successful. Token acquired")
        save_login_credentials(client_id=client_id, client_secret=client_secret)

        click.echo("Authentication successful. Credentials saved securely.")

    except Exception as e:
        logger.error(f"Error during authentication: {e}")


@cli.command()
@click.option("--bbox", nargs=4, type=float, required=True, help="Bounding box in [minLon, minLat, maxLon, maxLat].")
@click.option("--start-date", required=True, help="Start date in YYYY-MM-DD format.")
@click.option("--end-date", required=True, help="End date in YYYY-MM-DD format.")
@click.option("--satellite-type", required=True, type=click.Choice(["sentinel-2-l2a", "sentinel-2-l1c"]), help="Satellite type.")
@click.option("--output-type", default="NDVI", type=click.Choice(["NDVI", "VISUAL"]), help="type for image output. eg. NDVI or VISUAL")
@click.option("--output-format", default="PNG", type=click.Choice(["PNG", "TIFF"]), help="Output image format eg PNG or TIFF.")
@click.option("--output-file", default="output_image.png", help="Output file name for the downloaded image.")
def getimages(
    bbox: List[float], 
    start_date: str, 
    end_date: str, 
    satellite_type: str, 
    output_type: str, 
    output_format: str, 
    output_file: Optional[str] = None
    ):
    
    """
        Fetch and save images from Sentinel Hub.
    """
    try:
        logger.info("Fetching login credentials...")
        login_credentials = read_login_credentials()
        token = LoginAuth(login_credentials).get_token()["access_token"]

        if not validate_bbox(bbox):
            raise ValueError("Invalid bounding box provided.")

        logger.info("Creating request data...")

        file_extensions_mapping = {"PNG": ".png", "TIFF": ".tiff"}
        file_extension = file_extensions_mapping.get(output_format.upper(), ".png")

        if not output_file.endswith(file_extension):
            output_file += file_extension

        request_data = create_request_data(
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            maxCloudCoverage=20,  
            mosaickingOrder="leastCC",
            satellite_type=satellite_type,
            eval_type=output_type,
            output_format=output_format
        )

        logger.info("Processing request to fetch the image...")
        process_request(token=token, data=request_data, output_file=output_file)
        click.echo(f"Image saved as {output_file}")

    except Exception as e:
        logger.error(f"Error fetching image: {e}")
        click.echo(f"Error fetching image: {e}", err=True)


@cli.command()
@click.option("--bbox", nargs=4, type=float, required=True, help="Bounding box in [minLon, minLat, maxLon, maxLat].")
@click.option("--start-date", required=True, help="Start date in YYYY-MM-DD format.")
@click.option("--end-date", required=True, help="End date in YYYY-MM-DD format.")
def catalog_s(bbox: List[float], start_date: str, end_date: str):

    """
     Generate statistics for the available features.

    """
    try:
        logger.info("Fetching login credentials...")
        login_credentials = read_login_credentials()
        token = LoginAuth(login_credentials).get_token()["access_token"]

        if not validate_bbox(bbox):
            raise ValueError("Invalid bounding box provided.")
        
        logger.info("Creating catalog request data...")
        
        datetime = f"{start_date}T00:00:00Z/{end_date}T23:59:59Z"

        response = catalog_request(
            token=token,
            collections=["sentinel-2-l2a"],
            datetime=datetime,
            bbox=bbox,
            limit=10,  
            cloud_cover=20  
        )

        logger.info("Extracting and displaying statistics...")
        
        statistics = extract_statistics(response)
        click.echo("Catalog Results:")
        click.echo(json.dumps(statistics, indent=4))

    except Exception as e:
        logger.error(f"Error generating statistics: {e}")
        click.echo(f"Error generating statistics: {e}", err=True)




if __name__ == "__main__":
    cli()
