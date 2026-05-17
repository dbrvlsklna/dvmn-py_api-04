import os
import argparse
import requests
from save_images_helpers import save_image, get_image_extension
from dotenv import load_dotenv


NASA_API_URL = "https://api.nasa.gov/planetary/apod"


def fetch_daily_astronomy_images(token, proxies, count, save_path):
    params = {"api_key": token, "count": count}
    response = requests.get(NASA_API_URL, proxies=proxies, params=params)
    response.raise_for_status()
    daily_images_links = [item.get("url") for item in response.json()]
    for link_number, link in enumerate(daily_images_links):
        extension = get_image_extension(link)
        image_response = requests.get(link, proxies=proxies)
        image_response.raise_for_status()
        image_name = f"nasa_apod_{link_number}.{extension}"
        save_image(save_path, image_response.content, image_name)
    return daily_images_links


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Скрипт для скачивания астрономических изображений дня (NASA)"
    )
    parser.add_argument(
        "dir_path", help="Путь до директории для сохранения изображений"
    )
    parser.add_argument("count", help="Количество изображений для скачивания")
    args = parser.parse_args()
    try:
        token = os.environ["NASA_TOKEN"]
        proxies = {
            "http": os.environ["HTTP_PROXY"],
            "https": os.environ["HTTP_PROXY"],
        }
        fetch_daily_astronomy_images(
            token, proxies, args.count.strip(), args.dir_path.strip()
        )
    except KeyError as error:
        exit(f"Переменная окружения не существует: {error}")
    except requests.exceptions.HTTPError as error:
        exit(f"Не удалось получить данные: {error}")
    except requests.exceptions.RequestException as error:
        exit(f"Возникла ошибка: {error}")


if __name__ == "__main__":
    main()


