import json
import zipfile
import time
from pathlib import Path


def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, pluginfile_path: Path, scheme='http'):
    manifest_dict = {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version": "22.0.0"
    }

    manifest_json = json.dumps(manifest_dict, indent=4)

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "{scheme}",
                host: "{proxy_host}",
                port: parseInt("{proxy_port}")
            }},
            bypassList: ["localhost"]
        }},
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{proxy_username}",
                password: "{proxy_password}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    with zipfile.ZipFile(pluginfile_path, 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', background_js)

    # Проверка, что файл действительно записан
    time.sleep(0.1)
    if not pluginfile_path.exists() or pluginfile_path.stat().st_size < 100:
        raise RuntimeError(f"Плагин не создан или пустой: {pluginfile_path}")

    print(f"Создан плагин: {pluginfile_path} ({pluginfile_path.stat().st_size} байт)")

    return pluginfile_path