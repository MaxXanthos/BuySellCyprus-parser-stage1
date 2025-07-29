import json
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from sqlalchemy import create_engine, Column, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

from driver_manager import get_driver_with_proxy
from progress_manager import ProgressManager


# ───────────────────────────────
# CONFIGURATION
# ───────────────────────────────

MAX_PAGES = 100
BASE_URLS = [
    "https://www.buysellcyprus.com/properties-for-sale/type-apartment/page-{}",
    "https://www.buysellcyprus.com/properties-for-sale/type-house/page-{}"
]
PROXY_FILE = "many_proxy.json"
DATABASE_URL = "postgresql+psycopg2://postgres:123123000@localhost:5432/postgres"
FAILED_ROWS_FILE = Path("failed_rows.csv")
THREADS = 5

# ───────────────────────────────
# DATABASE SETUP
# ───────────────────────────────
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class BuySellCyprus1(Base):
    __tablename__ = "buysellcyprus1"
    id = Column(Text, primary_key=True)
    link = Column(Text, nullable=True)
    date_and_time = Column(DateTime, default=datetime.now(timezone.utc))

# ───────────────────────────────
# PARSING FUNCTIONS
# ───────────────────────────────
def process_page(url: str, proxy_data: dict, page_num: int):
    print(f"[{time.time()}] [Thread {threading.get_ident()}] Обработка страницы {page_num}")
    print(f"Прокси: {proxy_data['proxy_address']}:{proxy_data['port']}")

    driver, pluginfile_path = get_driver_with_proxy(proxy_data)
    next_page_url = None
    results_on_page = []

    try:
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "section[id^='listingItem']"))
            )
            print("Объявления на странице загружены")

        except TimeoutException:
            print("Cloudflare или другая защита. Объявления не появились.")
            return None

        elements = driver.find_elements(By.CSS_SELECTOR, "section[id^='listingItem']")
        for item in elements:
            try:
                links = item.find_elements(By.CSS_SELECTOR, "a[href*='/property-for-sale/']")
                hrefs = [el.get_attribute("href") for el in links if el.get_attribute("href")]
                final_link = next((l for l in hrefs if not l.endswith("/gallery")), "N/A")

                listing_id = "N/A"
                for span in item.find_elements(By.CSS_SELECTOR, "span"):

                    text = span.text.strip()
                    if "ID:" in text:
                        listing_id = text.split("ID:")[-1].replace(")", "").strip()
                        break

                results_on_page.append((listing_id, final_link))
            except Exception as e:
                print(f"Ошибка в элементе: {e}")

        try:
            next_button = driver.find_element(By.ID, "NextPage")
            next_page_url = next_button.get_attribute("href")
            print(f"Следущая страница: {next_page_url}")
        except NoSuchElementException:
            print("Кнопка 'Next' не найдена.")
        except Exception as e:
            print(f"Ошибка при поиске 'Next': {e}")

    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
    finally:
        driver.quit()
        if pluginfile_path.exists():
            pluginfile_path.unlink(missing_ok = True)
            print("Удалён временный плагин с прокси.")

    return next_page_url, results_on_page


def process_page_threaded(page_num: int, proxy: dict, base_url: str, progress: ProgressManager):
    url = base_url.format(page_num)
    retry_count = 3

    for attempt in range(1, retry_count + 1):
        try:
            next_url, results = process_page(url, proxy, page_num)
            progress.add_listings(results)
            progress.mark_page_processed(page_num)
            return next_url, results
        except Exception as e:
            print(f"Ошибка на странице {page_num}, попытка {attempt}: {e}")
            time.sleep(2)

    print(f"Страница {page_num} не обработана после {retry_count} попыток.")
    return None, []


# ───────────────────────────────
# DATABASE INSERTION
# ───────────────────────────────
from typing import List, Tuple # if python < python 3.9
def save_to_database(listings: list[tuple[str, str]]):
    session = Session()
    success, failed = 0, 0

    for listing_id, link in listings:
        if listing_id == "N/A" or link == "N/A":
            continue
        try:
            row = BuySellCyprus1(
                id=str(listing_id),
                link=link,
                date_and_time=datetime.now(timezone.utc)
            )
            session.merge(row)
            success += 1
        except Exception as e:
            print(f"[ERROR] {listing_id}: {e}")
            FAILED_ROWS_FILE.write_text(f"{listing_id}, {link}\n")
            failed += 1

    try:
        session.commit()
        print(f"\n Успешно в базе: {success} записей")
        if failed:
            print(f"⚠️ Не удалось записать: {failed} (см. {FAILED_ROWS_FILE})")
    except Exception as e:
        session.rollback()
        print(f"[COMMIT ERROR]: {e}")
    finally:
        session.close()


# ───────────────────────────────
# MAIN EXECUTION
# ───────────────────────────────
def main():
    start = time.time()

    with open(PROXY_FILE, "r", encoding="utf-8") as f:
        proxies = json.load(f)
    if not proxies:
        raise RuntimeError("Файл с прокси пуст или не существует")

    progress = ProgressManager()
    listings = []

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [
            executor.submit(process_page_threaded, page_num, random.choice(proxies), base_url, progress)
            for base_url in BASE_URLS
            for page_num in range(1, MAX_PAGES + 1)
        ]

        for future in as_completed(futures):
            try:
                _, page_results = future.result()
                if page_results:
                    listings.extend(page_results)
            except Exception as e:
                print (f"Ошибка в потоке: {e}")

    for listing_id, link in listings:
        print(f"ID: {listing_id} | URL: {link}")

    save_to_database(listings)
    print(f"\nЗавершено за {time.time() - start:.2f} секунд")

if __name__ == "__main__":
    main()