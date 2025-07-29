from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read("config.ini")

# ────────────── Общие настройки ──────────────
MAX_RETRIES = config.getint("general", "MAX_RETRIES")
THREADS = config.getint("general", "THREADS")
MAX_PAGES = config.getint("general", "MAX_PAGES")
DATABASE_URL = config.get("general", "DATABASE_URL")
WEBSHAREIO_PROXY_API_KEY = config.get("general", "WEBSHAREIO_PROXY_API_KEY")

# ────────────── Парсер ──────────────
WEBDRIVER_PATH = config.get("parser", "webdriver_path")

# ────────────── Логирование ──────────────
LOG_LEVEL = config.get("logging", "log_level")
LOG_FILE = Path(config.get("logging", "log_file"))

# ────────────── Файлы ──────────────
FAILED_ROWS_FILE = Path(config.get("files", "FAILED_ROWS_FILE"))
PROXY_FILE = Path(config.get("files", "PROXY_FILE"))
PROGRESS_FILE = Path(config.get("files", "PROGRESS_FILE"))