import requests, os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')
lat_lon_cu = '55.768760, 37.588817'
def get_local_key(lat_lon):
    url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
    params = {
        'apikey': API_KEY,
        'q': lat_lon,
        'language': 'ru-ru',
        'details': 'true'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data['Key']
    except KeyError:
        print("Не удалось найти ключ в ответе API")

    return None

print(get_local_key(lat_lon_cu))

def get_weather(local_key):
    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{local_key}'
    params = {
        'apikey': API_KEY,
        'language': 'ru-ru',
        'details': 'true'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except KeyError:
        print(f"Ошибка")
    return None

def get_weather_lat_lon(lat_lon):
    local_key = get_local_key(lat_lon)
    if not local_key:
        return {"error": "Не удалось получить локальный ключ"}
    weather = get_weather(local_key)
    return weather

def get_summary_weather(json_weather):
    real_feel_temperature = float(json_weather["RealFeelTemperature"]["Value"])
    wind_speed = float(json_weather["Wind"]["Speed"]["Value"]) * 1.61
    rain_probability = float(json_weather["RainProbability"])
    visibility = float(json_weather["Visibility"]["Value"])
    return {
            "temperature": real_feel_temperature,
            "wind": wind_speed,
            "rain_probability": rain_probability
    }

def check_bad_weather(temperature, wind_speed, rain_probability, visibility):
    if temperature < 2 or temperature > 35:
        return "Плохие погодные условия: температура вне норм"
    if wind_speed > 49:
        return "Плохие погодные условия: сильный ветер"
    if rain_probability > 85:
        return "Плохие погодные условия: высокая вероятность осадков"
    return "Хорошие погодные условия."