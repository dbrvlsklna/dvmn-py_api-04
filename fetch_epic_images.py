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
    images_metadata = requests.get(EPIC_API_URL, proxies=proxies, params=params)
    images_metadata.raise_for_status()
    for image_number, image in enumerate(images_metadata):
        date = datetime.strptime(image["date"], "%Y-%m-%d %H: %M: %S")
        image_name = image["image"]
        image_download_link = f"{EPIC_DOWNLOAD_IMAGE_API_URL}/{date.year}/{date.month}/{date.day}/png/{image_name}.png"
        image_response = requests.get(image_download_link, proxies=proxies)
        image_response.raise_for_status()
        save_image(save_path, image_response.content, image_name)
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
    try:
        token = os.environ["NASA_TOKEN"]
        proxies = {
            "http": os.environ["HTTP_PROXY"],
            "https": os.environ["HTTP_PROXY"],
        }
        fetch_epic_images(token, proxies, args.dir_path.strip())
    except KeyError as error:
        exit(f"Переменная окружения не существует: {error}")
    except requests.exceptions.HTTPError as error:
        exit(f"Не удалось получить данные: {error}")
    except requests.exceptions.RequestException as error:
        exit(f"Возникла ошибка: {error}")


if __name__ == "__main__":
    main()
