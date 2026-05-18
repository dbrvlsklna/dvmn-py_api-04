import os
import argparse
import requests
from datetime import datetime
from save_images_helpers import save_image, get_image_extension
from dotenv import load_dotenv


EPIC_API_URL = "https://api.nasa.gov/EPIC/api/natural"
EPIC_DOWNLOAD_IMAGE_API_URL = "https://api.nasa.gov/archive/natural"


def fetch_epic_images(token, proxies, save_path):
    params = {"api_key": token}
    response = requests.get(EPIC_API_URL, proxies=proxies, params=params)
    response.raise_for_status()
    images_metadata = response.json()
    for image_number, image in enumerate(images_metadata):
        date = datetime.strptime(image["date"], "%Y-%m-%d %H: %M: %S")
        image_name = image["image"]
        image_download_link = f"{EPIC_DOWNLOAD_IMAGE_API_URL}/{date.year}/{date.month}/{date.day}/png/{image_name}.png"
        image_response = requests.get(image_download_link, proxies=proxies)
        image_response.raise_for_status()
        full_image_name = f"{image_name}.png"
        save_image(save_path, image_response.content, full_image_name)
    return images_metadata


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Скрипт для скачивания EPIC изображений (NASA)"
    )
    parser.add_argument(
        "dir_path", help="Путь до директории для сохранения изображений"
    )
    args = parser.parse_args()
    dir_path = args.dir_path.strip()
    token = os.environ.get("NASA_TOKEN")
    if not token:
        exit("Не задана переменная окружения NASA_TOKEN")
    proxy_url = os.environ.get("HTTP_PROXY")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    try:
        fetch_epic_images(token, proxies, dir_path)
    except requests.exceptions.HTTPError as error:
        exit(f"Не удалось получить данные: {error}")
    except requests.exceptions.RequestException as error:
        exit(f"Возникла ошибка: {error}")


if __name__ == "__main__":
    main()
