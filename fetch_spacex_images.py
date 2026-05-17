import os
import argparse
import requests
from dotenv import load_dotenv
from save_images_helpers import save_image, get_image_extension


BASE_SPACEX_API_URL = "https://api.spacexdata.com/v5/launches"


def fetch_spacex_last_launch(save_path, proxies, launch_id=None):
    if launch_id is None:
        launch_id = "latest"
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
        description="Скрипт для скачивания фото запусков с сайта SpaceX"
    )
    parser.add_argument("dir_path", help="Путь до директории для сохранения фото")
    parser.add_argument("-id", "--launch_id", help="Идентификатор запуска")
    args = parser.parse_args()
    try:
        proxies = {
            "http": os.environ["HTTP_PROXY"],
            "https": os.environ["HTTP_PROXY"],
        }
        fetch_spacex_last_launch(args.dir_path.strip(), proxies, args.launch_id)
    except KeyError as error:
        exit(f"Переменная окружения не существует: {error}")
    except ValueError as error:
        exit(f"Ошибка при получении данных от API SpaceX: {error}")        
    except requests.exceptions.HTTPError as error:
        exit(f"Не удалось получить данные: {error}")
    except requests.exceptions.RequestException as error:
        exit(f"Возникла ошибка: {error}")


if __name__ == "__main__":
    main()
