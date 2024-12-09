
from flask import Flask, render_template, request
from weather_city import get_weather_lat_lon, get_summary_weather, check_bad_weather

app = Flask(__name__)


def validate_coordinates(coords):
    try:
        lat, lon = map(float, coords.split(', '))
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True
    except ValueError:
        return False
    return False


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message=None)


@app.route('/weather', methods=['POST'])
def weather():
    start_city = request.form['start']
    end_city = request.form['end']

    # Валидация координат
    if not validate_coordinates(start_city):
        return render_template('index.html',
                               message='Введите корректные координаты (широта, долгота) для начальной точки.')

    if not validate_coordinates(end_city):
        return render_template('index.html',
                               message='Введите корректные координаты (широта, долгота) для конечной точки.')

    # Получаем данные о погоде
    try:
        json_weather_start = get_weather_lat_lon(start_city)
        json_weather_end = get_weather_lat_lon(end_city)

        if "error" in json_weather_start or "error" in json_weather_end:
            return render_template('index.html',
                                   message="Ошибка получения данных о погоде. Проверьте введенные координаты.")

        # Получаем сводку о погоде
        summary_start = get_summary_weather(json_weather_start)
        summary_end = get_summary_weather(json_weather_end)

        # Проверяем погодные условия
        weather_condition_start = check_bad_weather(
            summary_start["temperature"],
            summary_start["wind"],
            summary_start["rain_probability"]
        )
        weather_condition_end = check_bad_weather(
            summary_end["temperature"],
            summary_end["wind"],
            summary_end["rain_probability"]
        )

        message = f"Погода в {start_city}: {weather_condition_start}<br> Погода в {end_city}: {weather_condition_end}"
        return render_template('index.html', message=message)

    except Exception as e:
        return render_template('index.html', message=f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
