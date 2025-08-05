import json
import os
import time
import requests
import configparser
from urllib.parse import urlparse
from typing import List, Dict

from proxy_manager.many_proxy import fetch_all_webshare_proxies
from config import WEBSHAREIO_PROXY_API_KEY

config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'config.ini')
config_path = os.path.normpath(config_path)
config.read(config_path)

WEBSHAREIO_PROXY_API_KEY = WEBSHAREIO_PROXY_API_KEY

def parse_proxy(proxy_str: str) -> Dict[str, str]:
    """
    Разбирает строку прокси в словарь с ключами:
    username, password, proxy_address, port.

    Пример входа:
        "http://user:pass@123.45.67.89:8080"

    :param proxy_str: Прокси строка.
    :return: Словарь с данными прокси.
    """
    parsed = urlparse(proxy_str)
    return {
        "username": parsed.username,
        "password": parsed.password,
        "proxy_address": parsed.hostname,
        "port": parsed.port
    }


def save_proxies_to_json(many_proxy: List[str], output_path: str = "many_proxy.json") -> None:
    """
    Сохраняет список строк-прокси в формате JSON с разобранными полями.

    :param proxies: Список строк вида "http://user:pass@ip:port"
    :param output_path: Путь к JSON-файлу для сохранения.
    """
    proxies_dicts = [parse_proxy(p) for p in many_proxy]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(proxies_dicts, f, ensure_ascii=False, indent=4)

def fetch_all_webshare_proxies_with_retry(api_key: str, retries=5, backoff=5) -> List[str]:
    for attempt in range(1, retries + 1):
        try:
            proxies = fetch_all_webshare_proxies(api_key)
            print(f"Успешно загружено {len(proxies)} прокси")
            return proxies
        except requests.exceptions.ConnectionError as e:
            print(f"[Попытка {attempt}/{retries}] Ошибка соединения: {e}")
        except Exception as e:
            print(f"[Попытка {attempt}/{retries}] Неизвестная ошибка: {e}")

        sleep_time = backoff * attempt
        print(f"Ждем {sleep_time} секунд перед новой попыткой...")
        time.sleep(sleep_time)

    raise ConnectionError(f"Не удалось получить прокси после {retries} попыток")

if __name__ == "__main__":
    proxies = fetch_all_webshare_proxies_with_retry(WEBSHAREIO_PROXY_API_KEY)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    output_dir = os.path.join(project_root, "data")

    # Создаем директорию, если её нет
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "many_proxy.json")
    save_proxies_to_json(proxies, output_path)