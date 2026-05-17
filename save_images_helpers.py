import os
from pathlib import Path
from urllib.parse import urlsplit, unquote


def save_image(dir_path, image_bytes, image_name):
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    with open(f"{dir_path}/{image_name}", "wb") as file:
        file.write(image_bytes)


def get_image_extension(link):
    url_path_decoded = unquote(urlsplit(link).path)
    extension = os.path.splitext(url_path_decoded)[1].lstrip(".")
    return extension
