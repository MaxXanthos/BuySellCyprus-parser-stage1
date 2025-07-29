# BuySell Parser (Stage 1)

Парсер недвижимости с сайта [BuySellCyprus](https://www.buysellcyprus.com).  
Собирает ID и ссылки на объявления (дома и квартиры) и сохраняет их в базу данных PostgreSQL.  

---

## Возможности

- Поддержка прокси (сейчас Webshare)  
- Обход Cloudflare и других защит от ботов (через selenium-stealth и прокси)  
- Автоматическая настройка и управление WebDriver  
- Устойчивость к сбоям и таймаутам  

## Установка для запуска


## структура проекта

- BuySell_Project/
  - core/ — Логика драйвера и управления прогрессом
    - __init__.py
    - driver_manager.py
    - progress_manager.py
  - proxy_manager/ — Всё, что связано с прокси
    - __init__.py
    - many_proxy.py
    - proxy_writer.py
  - data/ — Файлы с данными
    - many_proxy.json
    - progress.json
  - main.py
  - README.md