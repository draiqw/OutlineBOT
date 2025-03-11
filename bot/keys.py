# keys.py

import requests
from constants import BASE_API_URL

def create_outline_key(name=""):
    """
    Создаёт новый ключ Outline.
    Если передано имя, добавляет его в payload.
    """
    url = f"{BASE_API_URL}/access-keys"
    headers = {"Content-Type": "application/json"}
    payload = {}
    if name:
        payload["name"] = name
    try:
        response = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        if response.status_code in (200, 201):
            data = response.json()
            access_url = data.get("accessUrl")
            return access_url if access_url else "Не удалось получить ключ из ответа API."
        else:
            return f"Ошибка API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Ошибка запроса: {e}"

