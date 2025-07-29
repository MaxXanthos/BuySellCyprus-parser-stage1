# BuySell Parser (Stage 1)

Парсер недвижимости с сайта [BuySellCyprus](https://www.buysellcyprus.com).  
Собирает ID и ссылки на объявления (дома и квартиры) и сохраняет их в базу данных PostgreSQL.  

---

## Возможности

- Поддержка прокси (сейчас Webshare)  
- Обход Cloudflare и других защит от ботов (через selenium-stealth и прокси)  
- Автоматическая настройка и управление WebDriver  
- Устойчивость к сбоям и таймаутам  

---

## Установка для запуска

1. **Клонируйте репозиторий**
    ```bash
    git clone https://github.com/MaxXanthos/BuySellCyprus-parser.git
    cd BuySell_Project
    ```
2. **Создайте и активируйте виртуальное окружение**
   - На Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - На macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Установите необходимые зависимости**
    ```bash
    pip install -r requirements.txt
    ```
4. **(Если используете Playwright) Установите браузеры:**
    ```bash
     playwright install
     ```
5. **Настройте конфигурацию**
   - отредактируйте файл `config.ini`, указав свои параметры.
6. **Запустите парсер**
    ```bash
    python main.py
    ```

---

## структура проекта

- BuySell_Project/
  - core/ — Логика драйвера и управления прогрессом
    - __init__.py
    - driver_manager.py
    - progress_manager.py
  - data/ — Файлы с данными
    - many_proxy.json
    - progress.json
    - failed_rows.csv
  - extensions/
    - __init__.py
    - proxy_extension.py
  - proxy_manager/ — Всё, что связано с прокси
    - __init__.py
    - many_proxy.py
    - proxy_writer.py
  - main.py
  - README.md
  - config.ini
  - settings.py

---

## Обратная связь
Если вы нашли ошибку или хотите предложить улучшение, откройте [issue](https://github.com/MaxXanthos/BuySellCyprus-parser/issues).
