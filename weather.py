import requests

LOCATION = 52.23, 21.00
BASE_URL = "https://api.open-meteo.com/v1/forecast" \
           "?latitude={latitude}&longitude={longitude}&timezone=auto" \
           "&current_weather=true" \
           "&daily=temperature_2m_min,temperature_2m_max"

status_codes = {
    0: "Bezchmurnie",
    1: "Trochę chmur",
    2: "Sporo chmur",
    3: "Pochmurnie",
    45: "Mgła",
    51: "Mżawka",
    61: "Lekki deszcz",
    63: "Średni deszcz",
    65: "Mocny deszcz",
    71: "Lekki śnieg",
    73: "Średni śnieg",
    75: "Mocny śnieg",
    95: "Burza",
    96: "Lekki grad",
    99: "Mocny grad",
}

relative_day_names = ["Dziś", "Jutro", "Pojutrze"]


def get_weather_lines() -> list[str]:
    url = BASE_URL.format(latitude=LOCATION[0], longitude=LOCATION[1])
    response = requests.get(url).json()
    current_temp = round(response["current_weather"]["temperature"])
    status_code = response["current_weather"]["weathercode"]
    status = status_codes.get(status_code, f"status #{status_code}")

    lines = [f"{current_temp}° {status}"]

    for i in range(3):
        day_name = relative_day_names[i]
        temp_min = round(response['daily']['temperature_2m_min'][i])
        temp_max = round(response['daily']['temperature_2m_max'][i])
        lines.append(f"{day_name}: {temp_max}°/{temp_min}°")

    return lines
