from typing import Dict, Optional
import logging

from shcli.utils.utils import validate_bbox



logger = logging.getLogger(__name__) 

def get_evalscript(eval_type:str ="VISUAL")-> str:
    """
    Returns the appropriate evalscript based on the eval_type.

    Args:
        eval_type (str): The type of evalscript to return ("VISUAL" or "NDVI").
    """
    ndvi_eval = """
    //VERSION=3
    function setup() {
      return {
        input: [{
          bands:["B04", "B08"],
        }],
        output: {
          id: "default",
          bands: 3,
        }
      }
    }

    function evaluatePixel(sample) {
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04)

        if (ndvi<-0.5) return [0.05,0.05,0.05]
        else if (ndvi<-0.2) return [0.75,0.75,0.75]
        else if (ndvi<-0.1) return [0.86,0.86,0.86]
        else if (ndvi<0) return [0.92,0.92,0.92]
        else if (ndvi<0.025) return [1,0.98,0.8]
        else if (ndvi<0.05) return [0.93,0.91,0.71]
        else if (ndvi<0.075) return [0.87,0.85,0.61]
        else if (ndvi<0.1) return [0.8,0.78,0.51]
        else if (ndvi<0.125) return [0.74,0.72,0.42]
        else if (ndvi<0.15) return [0.69,0.76,0.38]
        else if (ndvi<0.175) return [0.64,0.8,0.35]
        else if (ndvi<0.2) return [0.57,0.75,0.32]
        else if (ndvi<0.25) return [0.5,0.7,0.28]
        else if (ndvi<0.3) return [0.44,0.64,0.25]
        else if (ndvi<0.35) return [0.38,0.59,0.21]
        else if (ndvi<0.4) return [0.31,0.54,0.18]
        else if (ndvi<0.45) return [0.25,0.49,0.14]
        else if (ndvi<0.5) return [0.19,0.43,0.11]
        else if (ndvi<0.55) return [0.13,0.38,0.07]
        else if (ndvi<0.6) return [0.06,0.33,0.04]
        else return [0,0.27,0]
    }
    """

    visual_eval = """
    //VERSION=3
    function setup() {
      return {
        input: ["B02", "B03", "B04"],
        output: {
          bands: 3,
          sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
        }
      }
    }

    function evaluatePixel(sample) {
      return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
    }
    """
    
    return ndvi_eval if eval_type.upper() == "NDVI" else visual_eval

def create_request_data(
        bbox: list[float], 
        start_date: str, 
        end_date: str, 
        maxCloudCoverage: int, 
        mosaickingOrder: str, 
        satellite_type: str, 
        eval_type: str ="NDVI", 
        output_format="PNG",
        width: Optional[float] = 682.987,
        height: Optional[float] = 514.207
        )-> Dict:
    """
    Creates the request data based on user inputs.
    """
    if not validate_bbox(bbox):
        logger.error("Invalid bounding box provided. Aborting request.")
        return {}
    
    start_date_iso = f"{start_date}T00:00:00Z"
    end_date_iso = f"{end_date}T23:59:59Z"

    evalscript = get_evalscript(eval_type)

    format_mapping = {
        "TIFF": "image/tiff",
        "PNG": "image/png",
        "JPEG": "image/jpeg"
    }

    output_mime_type = format_mapping.get(output_format.upper(), "image/png") 

    data = {
        "input": {
            "bounds": {"bbox": bbox },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {"from": start_date_iso,"to": end_date_iso},
                        "maxCloudCoverage": maxCloudCoverage,
                        "mosaickingOrder": mosaickingOrder
                    },
                    "type": satellite_type
                }
            ]
        },
        "output": {
            "width": width,  
            "height": height,  
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": output_mime_type
                    }
                }
            ]
        },
        "evalscript": evalscript
    }

    return data