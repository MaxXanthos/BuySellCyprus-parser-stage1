# BuySell Parser (Stage 1)

Парсер недвижимости с сайта **BuySellCyprus**.  
Собирает `id` и ссылки на объявления (дома и квартиры), после чего сохраняет их в базу данных **PostgreSQL**.  
Поддерживает работу через прокси, умеет обходить защиту Cloudflare и автоматически управляет браузером Chrome.

---

## Возможности

- Поддержка прокси (сейчас Webshare)
- Обход Cloudflare и других защит от ботов (через selenium-stealth и прокси)
- Автоматическая настройка и управление WebDriver
- Устойчив к сбоям и таймаутам

## Установка для запуска


## структура проекта

BuySell_Project/
│
├── core/                      # логика драйвера, прогресса
│   ├── __init__.py
│   ├── driver_manager.py
│   └── progress_manager.py
│
├── proxy_manager/             # всё, что связано с прокси
│   ├── __init__.py
│   ├── many_proxy.py
│   └── proxy_writer.py
│
├── data/                      # файлы данных
│   ├── many_proxy.json
│   └── progress.json
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE (если решишь добавить)

└