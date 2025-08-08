# [general]
MAX_RETRIES = 3
THREADS = 5
MAX_PAGES = 30 # (24 objects per page and base_url 2 so it's actually x2 of what's written here)

DATABASE_URL = "postgresql+psycopg2://postgres:123123000@localhost:5432/postgres"
WEBSHAREIO_PROXY_API_KEY = ""


# [parser]
WEBDRIVER_PATH = "chromedriver.exe"


# [files]
FAILED_ROWS_FILE = "data/failed_rows.csv"
PROXY_FILE = "data/many_proxy.json"
FAILED_PAGES_FILE = "data/failed_pages.txt"