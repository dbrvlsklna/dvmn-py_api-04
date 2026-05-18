import os
import random
import time
import argparse

import telegram
from telegram.error import TelegramError
from dotenv import load_dotenv


def get_all_images(img_dir):
    images_paths = []
    for root, dirs, images in os.walk(img_dir):
        for image in images:
            images_paths.append(os.path.join(root, image))
    return images_paths


def get_random_image(img_dir):
    images_paths = get_all_images(img_dir)
    return random.choice(images_paths)


def auto_posting_with_delay(chat_id, bot, img_dir, delay_seconds):
    while True:
        images_paths = get_all_images(img_dir)
        random.shuffle(images_paths)
        for img_path in images_paths:
            post_photo(chat_id, bot, img_path=img_path)
            time.sleep(delay_seconds)


def post_photo(chat_id, bot, img_path):
    with open(img_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Скрипт для публикации изображений космоса в Telegram канал"
    )
    parser.add_argument("img_dir", help="Путь до директории c изображениями")
    parser.add_argument("-i", "--img_path", help="Путь до изображения для публикации")
    parser.add_argument(
        "-a",
        "--auto_posting",
        action="store_true",
        help="Запустить автобуликацию изображений из директории",
    )
    parser.add_argument(
        "-d",
        "--delay_seconds",
        type=int,
        default=2,
        help="Интервал публикации и ожидания в секундах (по умолчанию: 4 часа/14400 секунд)",
    )
    args = parser.parse_args()
    auto_posting = args.auto_posting
    img_dir = args.img_dir.strip()
    img_path = args.img_path.strip() if args.img_path else None
    delay_seconds = args.delay_seconds
    token = os.environ.get("TG_TOKEN")
    chat_id = os.environ.get("TG_CHAT_ID")
    if not token or not chat_id:
        exit("Переменные окружения TG_TOKEN и TG_CHAT_ID должны быть заполнены")

    bot = telegram.Bot(token=token)

    try:
        if auto_posting:
            auto_posting_with_delay(chat_id, bot, img_dir, delay_seconds)
        else:
            if not img_path:
                img_path = get_random_image(img_dir)
            post_photo(chat_id, bot, img_path)
    except TelegramError as error:
        exit(f"Ошибка при обращении к API Telegram: {error}")


if __name__ == "__main__":
    main()
