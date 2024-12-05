from settings import GRATHHOPPER_KEY
import requests
import json
from geopy.distance import geodesic
from time import sleep

class RoadDistance:
    def __init__(self, api_key = GRATHHOPPER_KEY):
        self.api_key = api_key
        self.__MKAD_COORDINATES = [
            (55.639823, 37.456653),
            (55.611931, 37.489198),
            (55.574954, 37.592917),
            (55.573976, 37.596963),
            (55.590101, 37.726558),
            (55.683873, 37.832413),
            (55.705866, 37.834903),
            (55.711316, 37.837465),
            (55.741322, 37.842349),
            (55.775392, 37.843532),
            (55.811964, 37.839591),
            (55.881508, 37.729242),
            (55.895812, 37.675568),
            (55.909016, 37.592993),
            (55.908430, 37.546507),
            (55.893787, 37.498542),
            (55.882655, 37.448746),
            (55.871638, 37.412175),
            (55.849579, 37.392091),
            (55.833459, 37.394892),
            (55.832785, 37.394179),
            (55.793249, 37.375657),
            (55.772712, 37.369092),
            (55.766900, 37.368776),
            (55.714736, 37.384041),
            (55.663860, 37.430310),
            (55.574218, 37.684431),
            (55.734629, 37.374109),
            (55.889429, 37.484343),
            (55.893929, 37.500058),

        ]

    def __get_coord(self, loc):
        """Получение координат по адресу."""
        geocode_url = "https://graphhopper.com/api/1/geocode"
        geocode_params = {"key": self.api_key, "q": loc}
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_data = geocode_response.json()
        if geocode_data.get("hits"):
            lat = geocode_data["hits"][0]["point"]["lat"]
            lng = geocode_data["hits"][0]["point"]["lng"]
            sleep(1)
            return {'lng' :lng, 'lat' :lat}
        else:
             return {"error": f"Ошибка при геокодировании адреса: {loc}"}
    def get_distance(self, locations):
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
        if isinstance(locations, str):
            locations = json.loads(locations)
        for loc in locations:
            if isinstance(loc, dict) and "lat" in loc and "lng" in loc:
                points.append([loc["lng"], loc["lat"]])
            elif isinstance(loc, str) and '{' in loc:
                loc = json.loads(loc)  # Преобразование в словарь
                points.append([loc["lng"], loc["lat"]])
            elif isinstance(loc, str):
                    result = self.__get_coord(loc)
                    if not result.get("error"):
                        points.append([result["lng"], result["lat"]])
                    else:
                        return {"error": f"Ошибка при геокодировании адреса: {loc}"}

        payload = {
            "profile": "car",
            "points": points,
            "snap_preventions": ["ferry", "ford"]
        }
        query = {"key": self.api_key}
        response = requests.post(url, json=payload, headers=headers, params=query)

        if response.status_code == 200:
            data = response.json()
            if "paths" in data and data["paths"]:
                sleep(1)
                return {"distance": data["paths"][0]["distance"]}
            else:
                return {"error": "Нет маршрутов в ответе."}
        else:
            sleep(1)
            return {"error": f"HTTP {response.status_code} - {response.text}"}
        
    def __get_nearest(self, lng, lat, max_points = 3):
        """
        Получение ближайших точек съездов от МКАД
        """
        filtered_points = self.__MKAD_COORDINATES.copy()
        filtered_points.sort(key = lambda pt: geodesic(pt, (lat, lng)).km)
        return filtered_points[:max_points]
    
    def get_mkad_distance(self, location, max_points = 3):
        """
        Рассчитывает расстояние по дорогам от МКАД
        """
        if isinstance(location, str) and not '{' in location:
            location = self.__get_coord(location)
        elif isinstance(location, str):
            location= json.loads(location)
        if location.get("error"):
            return location
        dist = []
        points = self.__get_nearest(location["lng"], location["lat"],max_points)
        for point in points:
            result = self.get_distance([{'lat':point[0],'lng':point[1]}, location])
            if result.get("error"):
                return {"error": result.get("error")}
            else:
                dist.append(float(result.get("distance")))
        return {"distance": min(dist)}


