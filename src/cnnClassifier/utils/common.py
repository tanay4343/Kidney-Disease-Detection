import os
from box.exceptions import BoxValueError
import yaml
from src.cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns ConfigBox object
    Args:
        path_to_yaml (Path): path like input
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    Returns:
        ConfigBox: ConfigBox type object
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                raise ValueError(f"The YAML file at {path_to_yaml} is empty.")
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("The YAML file is empty")
    except Exception as e:
        raise e 
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """create directories from list of path
    Args:
        path_to_directories (list[Path]): list of path of directories
        ignore_log (bool, optional): ignore if multiple directories are to be created. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data to path
    Args:
        path (Path): path to save json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json file from path
    Args:
        path (Path): path to json file
    Returns:
        ConfigBox: ConfigBox type object
    """
    with open(path, "r") as f:
        content = json.load(f)
    logger.info(f"JSON file loaded from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(path: Path, data: Any):
    """save binary data to path using joblib
    Args:
        path (Path): path to save binary file
        data (Any): data to be saved
    """
    with open(path, "wb") as f:
        joblib.dump(data, f)
    logger.info(f"Binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data from path using joblib
    Args:
        path (Path): path to binary file
    Returns:
        Any: data loaded from binary file
    """
    with open(path, "rb") as f:
        data = joblib.load(f)
    logger.info(f"Binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size of file in KB
    Args:
        path (Path): path to file
    Returns:
        str: size of file in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"{size_in_kb:.2f} KB"

@ensure_annotations
def decodeImage(imgstring, fileName):
    """Decode a base64 string and save it as an image file.
    Args:
        imgstring (str): Base64 encoded string of the image.
        fileName (str): The name of the file to save the decoded image.
    """
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()
    logger.info(f"Image decoded and saved to: {fileName}")

@ensure_annotations
def encodeImageIntoBase64(croppedImagePath):
    """Encode an image file into a base64 string.
    Args:
        croppedImagePath (str): The path to the image file to be encoded.
    Returns:
        str: Base64 encoded string of the image.
    """
    with open(croppedImagePath, "rb") as f:
        b64_string = base64.b64encode(f.read()).decode('utf-8')
    logger.info(f"Image at {croppedImagePath} encoded into base64 string")
    return b64_string