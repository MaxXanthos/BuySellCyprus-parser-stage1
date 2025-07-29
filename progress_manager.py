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
        self.progress_file: str = progress_file
        self.processed_pages: set = self._load_progress()
        self.listings: list = []

    def _load_progress(self) -> set:
        """
        Загружает прогресс из файла, если он существует.
        :return: Множество номеров обработанных страниц
        """
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r") as f:
                    pages = json.load(f)
                    return set(pages)
            except Exception as e:
                print(f"Ошибка загрузки прогресса: {e}")
                return set()
        return set()

    def save_progress(self) -> None:
        """
        Сохраняет текущий прогресс в файл.
        """
        try:
            with open(self.progress_file, "w") as f:
                json.dump(list(self.processed_pages), f)
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
        Добавляет новые объявления к списку.

        Аргументы:
            new_listings (list): Список новых объявлений.
        """
        self.listings.extend(new_listings)

    def is_page_processed(self, page_num) -> bool:
        """
        Проверяет, была ли страница уже обработана.

        Аргументы:
            page_num (int): Номер страницы.

        Возвращает:
            bool: True, если страница уже была обработана.
        """
        return page_num in self.processed_pages