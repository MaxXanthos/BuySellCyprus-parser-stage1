import json
import os
from decimal import Decimal


class ProgressManager:
    """
    Управляет прогрессом обхода страниц:
    Сохраняет уже обработанные страницы и собранные объявления.
    """

    def __init__(self, progress_file: str = "progress.json"):
        self.PROGRESS_FILE: str = progress_file
        self.processed_pages: dict = {}
        self.listings: list = []
        self._load_progress()

    def _load_progress(self) -> None:
        if os.path.exists(self.PROGRESS_FILE):
            try:
                with open(self.PROGRESS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if not isinstance(data.get("processed_pages", {}), dict):
                        raise ValueError("Некорректный формат processed_pages")
                    if not isinstance(data.get("listings", []), list):
                        raise ValueError("Некорректный формат listings")

                    self.processed_pages = data.get("processed_pages", {})
                    self.listings = data.get("listings", [])
                    print(f"Загружено {len(self.processed_pages)} обработанных страниц и {len(self.listings)} объявлений")
            except Exception as e:
                print(f"Ошибка загрузки прогресса: {e}")
                self.processed_pages = {}
                self.listings = []
        else:
            self.processed_pages = {}
            self.listings = []

    def save_progress(self) -> None:
        try:
            data = {
                "processed_pages": self.processed_pages,
                "listings": [
                    [id_, link, float(price) if isinstance(price, Decimal) else price]
                    for id_, link, price in self.listings
                ]
            }
            with open(self.PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Прогресс успешно сохранён.")
        except Exception as e:
            print(f"Ошибка сохранения прогресса: {e}")

    def mark_page_processed(self, page_type: str, page_num: int) -> None:
        if page_type not in self.processed_pages:
            self.processed_pages[page_type] = []
        if page_num not in self.processed_pages[page_type]:
            self.processed_pages[page_type].append(page_num)
        self.save_progress()

    def add_listings(self, new_listings) -> None:
        self.listings.extend(new_listings)
        self.save_progress()

    def is_page_processed(self, page_type: str, page_num: int) -> bool:
        return page_num in self.processed_pages.get(page_type, [])