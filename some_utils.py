from pathlib import Path
from config import WEBDRIVER_PATH
from webdriver_manager.chrome import ChromeDriverManager

def get_chromedriver():
    path = Path(WEBDRIVER_PATH)
    if path.is_file():
        return str(path)
    else:
        return ChromeDriverManager().install()