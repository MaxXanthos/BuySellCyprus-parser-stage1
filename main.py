import json
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

# для цены
from decimal import Decimal, InvalidOperation

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from sqlalchemy import create_engine, Column, Text, Numeric, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

from core.driver_manager import get_driver_with_proxy

from config import MAX_PAGES, THREADS, DATABASE_URL, PROXY_FILE, FAILED_ROWS_FILE, WEBDRIVER_PATH, MAX_RETRIES, FAILED_PAGES_FILE

BASE_URLS = [
    "https://www.buysellcyprus.com/properties-for-sale/type-apartment/page-{}",
    "https://www.buysellcyprus.com/properties-for-sale/type-house/page-{}"
]


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
    price = Column(Numeric(15, 2), nullable=True)
    date_and_time = Column(DateTime, default=datetime.now(timezone.utc))

# ───────────────────────────────
# PARSING FUNCTIONS
# ───────────────────────────────
def process_page(url: str, proxy_data: dict, page_num: int):
    print(f"[Thread {threading.get_ident()}] Обработка страницы {page_num}")
    print(f"Прокси: {proxy_data['proxy_address']}:{proxy_data['port']}")

    driver, pluginfile_path = get_driver_with_proxy(proxy_data, WEBDRIVER_PATH)
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
            return None, []

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

                # парсим цену
                price = None
                try:
                    price_el = item.find_element(By.CSS_SELECTOR, ".bs-listing-info-price-base")
                    price_text = price_el.text.strip()
                    price_clean = (
                        price_text
                        .replace("€", "")
                        .replace(",", "")
                        .replace("\xa0", "")  # неразрывный пробел
                        .strip()
                    )
                    price = Decimal(price_clean)
                except (NoSuchElementException, InvalidOperation):
                    price = None

                results_on_page.append((listing_id, final_link, price))
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


def process_page_threaded(page_num: int, proxy: dict, base_url: str, page_type: str, progress):
    url = base_url.format(page_num)
    retry_count = MAX_RETRIES

    for attempt in range(1, retry_count + 1):
        try:
            next_url, results = process_page(url, proxy, page_num)
            return next_url, results
        except Exception as e:
            print(f"Ошибка на странице {page_num}, попытка {attempt}: {e}")
            time.sleep(2)

    print(f"Страница {page_num} не обработана после {retry_count} попыток.")
    with open(FAILED_PAGES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}\n")

    return None, []


# ───────────────────────────────
# DATABASE INSERTION
# ───────────────────────────────
def save_to_database(listings: list[tuple[str, str, Decimal | None]]):
    session = Session()
    success, failed = 0, 0

    for listing_id, link, price in listings:
        if listing_id == "N/A" or link == "N/A":
            continue
        try:
            row = BuySellCyprus1(
                id=str(listing_id),
                link=link,
                price=price,
                date_and_time=datetime.now(timezone.utc)
            )
            session.merge(row)
            success += 1
        except Exception as e:
            print(f"[ERROR] {listing_id}: {e}")
            with open(FAILED_ROWS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{listing_id}, {link}\n")
            failed += 1

    listing_id = "N/A"
    link = "N/A"

    try:
        session.commit()
        print(f"\nУспешно в базе: {success} записей")
        if failed:
            with open(FAILED_ROWS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{listing_id}, {link}\n")
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

    progress = None
    listings = []

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = []
        for base_url in BASE_URLS:
            if "type-apartment" in base_url:
                page_type = "apartment"
            elif "type-house" in base_url:
                page_type = "house"
            else:
                page_type = "unknown"

            for page_num in range(1, MAX_PAGES + 1):

                futures.append(
                    executor.submit(
                        process_page_threaded,
                        page_num,
                        random.choice(proxies),
                        base_url,
                        page_type,
                        progress
                    )
                )

        for future in as_completed(futures):
            try:
                _, page_results = future.result()
                if page_results:
                    listings.extend(page_results)
            except Exception as e:
                print(f"Ошибка в потоке: {e}")

    for listing_id, link, price in listings:
        print(f"ID: {listing_id} | Price: {price} | URL: {link}")

    save_to_database(listings)
    print(f"\nЗавершено за {time.time() - start:.2f} секунд")

if __name__ == "__main__":
    main()