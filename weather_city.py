import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

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
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except KeyError:
        print("Не удалось найти ключ в ответе API")

    return None

def get_weather(local_key):
    url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{local_key}'
    params = {
        'apikey': API_KEY,
        'language': 'ru-ru',
        'details': 'true'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()[0]
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except KeyError:
        print("Ошибка получения данных о погоде")

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
    return {
        "temperature": real_feel_temperature,
        "wind": wind_speed,
        "rain_probability": rain_probability
    }

def check_bad_weather(temperature, wind_speed, rain_probability):
    if temperature < 2 or temperature > 30:
        return "Плохие погодные условия: температура вне норм"
    if wind_speed > 49:
        return "Плохие погодные условия: сильный ветер"
    if rain_probability > 85:
        return "Плохие погодные условия: высокая вероятность осадков"
    return "Хорошие погодные условия."

#Тестирование

lat_lon = "54.2164817, -4.5390064"
weather = get_weather(get_local_key(lat_lon))
sum_weather = get_summary_weather(weather)
print(sum_weather)
temp = sum_weather['temperature']
wind = sum_weather['wind']
rain_prob = sum_weather['rain_probability']
print(check_bad_weather(temp, wind, rain_prob))