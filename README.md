# BuySell Parser (Stage 1)

Real estate parser from the [BuySellCyprus](https://www.buysellcyprus.com) website.
Collects IDs and links to ads (houses and apartments) and stories them in PostgreSQL database.

---

## Features

- Parses full property listing details from [BuySellCyprus](https://www.buysellcyprus.com)
- Proxy rotation support [Webshare](https://www.webshare.io/)
- Saves results to a PostgreSQL database
- Resistance to failures and timeouts
- Bypass Cloudflare and other bot protections (via selenium-stealth and proxy)
- Automatic configuration and management of WebDriver

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
   - Edit the `config.ini`file and set your database and parsing parameters.
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
    - many_proxy.json
    - progress.json
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
  - config.ini
  - settings.py

---

## Feedback
If you find a bug or want to suggest an improvement, open [issue](https://github.com/MaxXanthos/BuySellCyprus-parser/issues).