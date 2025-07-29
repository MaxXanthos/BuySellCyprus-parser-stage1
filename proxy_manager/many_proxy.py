import requests
import time

def fetch_all_webshare_proxies(api_key: str, per_page: int = 100, delay: float = 2) -> list:
    """
    Загружает все доступные прокси с Webshare.io с учетом пагинации.

    Parameters:
        api_key (str): API-ключ Webshare.
        per_page (int): Кол-во прокси на страницу (макс. 100).
        delay (float): Задержка между запросами в секундах.

    Returns:
        List[str]: Список готовых прокси в формате http://user:pass@ip:port
    """
    base_url = "https://proxy.webshare.io/api/v2/proxy/list/"
    headers = {
        "Authorization": f"Token {api_key}"
    }

    page = 1
    all_proxies = []

    while True:
        params = {
            "mode": "direct",
            "page": page,
            "limit": per_page
        }

        response = requests.get(base_url, headers=headers, params=params, timeout=30)

        if response.status_code != 200:
            print(f"Ошибка на странице {page}: {response.status_code} - {response.text}")
            break

        data = response.json()
        results = data.get("results", [])

        if not results:
            print("Все прокси загружены.")
            break

        for proxy in results:
            ip = proxy['proxy_address']
            port = proxy['port']
            username = proxy['username']
            password = proxy['password']
            proxy_url = f"http://{username}:{password}@{ip}:{port}"
            all_proxies.append(proxy_url)

        print(f"Страница {page}: загружено {len(results)} прокси")
        page += 1
        time.sleep(delay)

    print(f"\nВсего прокси загружено: {len(all_proxies)}")
    return all_proxies


# 🔧 Пример использования
#WEBSHAREIO_PROXY_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
#working_proxies = fetch_all_webshare_proxies(WEBSHAREIO_PROXY_API_KEY)