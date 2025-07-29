import logging
import os
from configparser import ConfigParser

def setup_logger():
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')

    log_level = config.get('logging', 'log_level', fallback='INFO').upper()
    log_file = config.get("logging", "log_file", fallback="parser.log")

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("parser_logger")
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger