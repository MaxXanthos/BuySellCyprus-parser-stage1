import json
import os

class ProgressManager:
    """
    Управляет прогрессом обхода страниц:
    Сохраняет уже обработанные страницы и собранные объявления.
    """

    def __init__(self, progress_file: str = "progress.json"):
        """
        Инициализирует менеджер прогресса.

        Аргументы:
            progress_file (str): Путь к файлу для хранения прогресса.
        """
        self.PROGRESS_FILE: str = progress_file
        self.processed_pages: set = set()
        self.listings: list = []
        self._load_progress()

    def _load_progress(self) -> None:
        """
        Загружает прогресс из файла, если он существует.
        """
        if os.path.exists(self.PROGRESS_FILE):
            try:
                with open(self.PROGRESS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    pages = data.get("processed_pages", [])
                    self.processed_pages = set(pages)
                    self.listings = data.get("listings", [])
                    print(f"Загружено {len(self.processed_pages)} обработанных страниц и {len(self.listings)} объявлений")
            except Exception as e:
                print(f"Ошибка загрузки прогресса: {e}")
                self.processed_pages = set()
                self.listings = []
        else:
            self.processed_pages = set()
            self.listings = []

    def save_progress(self) -> None:
        """
        Сохраняет текущий прогресс в файл.
        """
        try:
            data = {
                "processed_pages": list(self.processed_pages),
                "listings": self.listings
            }
            with open(self.PROGRESS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения прогресса: {e}")

    def mark_page_processed(self, page_num) -> None:
        """
        Помечает страницу как обработанную и сохраняет прогресс.

        Аргументы:
            page_num (int): Номер страницы.
        """
        self.processed_pages.add(page_num)
        self.save_progress()

    def add_listings(self, new_listings) -> None:
        """
        Добавляет новые объявления к списку и сохраняет прогресс.

        Аргументы:
            new_listings (list): Список новых объявлений.
        """
        self.listings.extend(new_listings)
        self.save_progress()

    def is_page_processed(self, page_num) -> bool:
        """
        Проверяет, была ли страница уже обработана.

        Аргументы:
            page_num (int): Номер страницы.

        Возвращает:
            bool: True, если страница уже была обработана.
        """
        return page_num in self.processed_pages