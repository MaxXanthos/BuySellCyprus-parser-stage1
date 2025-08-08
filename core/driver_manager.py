"""
Модуль для создания Selenium-драйвера с прокси и обходом Cloudflare.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from pathlib import Path
from extensions.proxy_extension import create_proxy_auth_extension
import os
from uuid import uuid4

from some_utils import get_chromedriver

CHROMEDRIVER_PATH = get_chromedriver()

def get_driver_with_proxy(proxy_data: dict, webdriver_path: str) -> tuple[webdriver.Chrome, Path]:

    """
    Создает драйвер с расширением авторизации прокси и включенной защитой от обнаружения.

    :param proxy_data: Словарь с ключами proxy_address, port, username, password
    :param webdriver_path: Путь к chromedriver
    :return: Кортеж из Selenium-драйвера и пути к ZIP-расширению
    """
    ip = proxy_data["proxy_address"]
    port = proxy_data["port"]
    username = proxy_data["username"]
    password = proxy_data["password"]

    plugin_path = Path(f"proxy_auth_plugin_{uuid4().hex}.zip")
    create_proxy_auth_extension(ip, port, username, password, plugin_path)

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_extension(str(plugin_path))

    driver = webdriver.Chrome(
        service=Service(CHROMEDRIVER_PATH),
        options=chrome_options
    )

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
    )

    return driver, plugin_path



def cleanup_plugin(plugin_path) -> None:
    """
    Удаляет ZIP-расширение прокси после использования.

    :param plugin_path: Путь к ZIP-файлу расширения
    """
    try:
        os.remove(plugin_path)
    except Exception as e:
        print(f"Ошибка при удалении расширения: {e}")