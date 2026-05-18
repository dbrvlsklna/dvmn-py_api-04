import os
import argparse
import requests
from dotenv import load_dotenv
from save_images_helpers import save_image, get_image_extension


BASE_SPACEX_API_URL = "https://api.spacexdata.com/v5/launches"


def fetch_spacex_images(save_path, proxies, launch_id="latest"):
    spacex_api_url = f"{BASE_SPACEX_API_URL}/{launch_id}"
    response = requests.get(spacex_api_url, proxies=proxies)
    response.raise_for_status()
    last_launch_images_links = response.json()["links"]["flickr"]["original"]
    if not last_launch_images_links:
        raise ValueError(f"Не удалось получить ссылки на фото для запуска {launch_id}")
    for link_number, link in enumerate(last_launch_images_links):
        extension = get_image_extension(link)
        image_response = requests.get(link, proxies=proxies)
        image_name = f"spacex_{link_number}.{extension}"
        save_image(save_path, image_response.content, image_name)
    return last_launch_images_links


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Скрипт для скачивания фото запусков ракет с сайта SpaceX"
    )
    parser.add_argument("dir_path", help="Путь до директории для сохранения фото")
    parser.add_argument(
        "-id",
        "--launch_id",
        default="latest",
        help="Идентификатор запуска (по умолчанию запрашивается последний запуск /latest)",
    )
    args = parser.parse_args()
    dir_path = args.dir_path.strip()
    launch_id = args.launch_id.strip()
    proxy_url = os.environ.get("HTTP_PROXY")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    try:
        fetch_spacex_images(dir_path, proxies, launch_id)
    except ValueError as error:
        exit(f"Ошибка при получении данных от API SpaceX: {error}")
    except requests.exceptions.HTTPError as error:
        exit(f"Не удалось получить данные: {error}")
    except requests.exceptions.RequestException as error:
        exit(f"Ошибка при обращении к API SpaceX: {error}")


if __name__ == "__main__":
    main()
