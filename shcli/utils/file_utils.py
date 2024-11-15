import logging

logger = logging.getLogger(__name__)

def save_image_to_file(content: bytes, output_file: str) -> None:
    """
    Saves binary content to a file.
    
    Args:
        content (bytes): The binary content to save.
        output_file (str): The path of the output file.
    """
    try:
        with open(output_file, "wb") as file:
            file.write(content)

        logger.info(f"Image successfully saved to {output_file}")

    except IOError as e:
        logger.error(f"Error saving the image to {output_file}: {e}")
