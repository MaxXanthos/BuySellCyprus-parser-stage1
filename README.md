# BuySell Parser (Stage 1)

Real estate parser from the [BuySellCyprus](https://www.buysellcyprus.com) website.
Collects IDs and links to ads (houses and apartments) and stories them in PostgreSQL database.

---

## Features

- Extracts:
  - Link
  - Price
  - URL
- Proxy rotation support [Webshare](https://www.webshare.io/)
- Saves results to a PostgreSQL database
- Resistance to failures and timeouts
- Bypass Cloudflare and other bot protections (via selenium-stealth and proxy)
- Automatic configuration and management of WebDriver
- Records pages that failed parsing into `failed_pages.txt` to allow manual checking and avoid interrupting the crawl

---

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/MaxXanthos/BuySellCyprus-parser.git
    cd BuySell_Project
    ```
2. **Create and activate a virtual environment**
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **(If using Playwright) Install browsers**
    ```bash
     playwright install
     ```
5. **Configure the project**
   - Edit the `config.py`file and set your database and parsing parameters.
   - Run the `proxy_writer.py` file to write your proxy

6. **Run the parser**
    ```bash
    python main.py
    ```

---

## Project structure

- BuySell_Project/
  - core/ — Driver logic and progress management
    - __init__.py
    - driver_manager.py
    - progress_manager.py
  - data/ — Data files
    - failed_pages.txt
    - many_proxy.json
    - progress_file.json
    - failed_rows.csv
  - extensions/
    - __init__.py
    - proxy_extension.py
  - proxy_manager/ — Everything related to proxies
    - __init__.py
    - many_proxy.py
    - proxy_writer.py
  - main.py
  - README.md
  - config.py
  - requirements.txt
  - some_utils

---

## Feedback
If you find a bug or want to suggest an improvement, open [issue](https://github.com/MaxXanthos/BuySellCyprus-parser1/issues).