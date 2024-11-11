from settings import GRATHHOPPER_KEY
import requests
import json

def get_distance(locations, api_key = GRATHHOPPER_KEY):
    """
    Рассчитывает расстояние по дорогам между списком координат или адресов с использованием GraphHopper API.

    Параметры:
        locations (list): Список координат (лат, лон) или адресов (строки).
        api_key (str): API-ключ для GraphHopper.

    Возвращает:
        dict: Содержит расстояние или сообщение об ошибке.
    """
    url = "https://graphhopper.com/api/1/route"
    headers = {"Content-Type": "application/json"}
    points = []

    for loc in json.loads(locations):
        if isinstance(loc, dict) and "lat" in loc and "lng" in loc:
            points.append([loc["lng"], loc["lat"]])
        elif isinstance(loc, str) and '{' in loc:
            loc = json.loads(loc)  # Преобразование в словарь
            points.append([loc["lng"], loc["lat"]])
        elif isinstance(loc, str):
            geocode_url = "https://graphhopper.com/api/1/geocode"
            geocode_params = {"key": api_key, "q": loc}
            geocode_response = requests.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()
            if geocode_data.get("hits"):
                lat = geocode_data["hits"][0]["point"]["lat"]
                lng = geocode_data["hits"][0]["point"]["lng"]
                points.append([lng, lat])
            else:
                return {"error": f"Ошибка при геокодировании адреса: {loc}"}

    payload = {
        "profile": "car",
        "points": points,
        "snap_preventions": ["ferry", "ford"]
    }
    query = {"key": api_key}
    response = requests.post(url, json=payload, headers=headers, params=query)

    if response.status_code == 200:
        data = response.json()
        if "paths" in data and data["paths"]:
            return {"distance": data["paths"][0]["distance"]}
        else:
            return {"error": "Нет маршрутов в ответе."}
    else:
        return {"error": f"HTTP {response.status_code} - {response.text}"}
