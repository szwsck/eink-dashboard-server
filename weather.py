import requests

from config import WEATHER_URL, WEATHER_STATUS_CODES, RELATIVE_DAY_NAMES


def get_weather_lines() -> list[str]:
    response = requests.get(WEATHER_URL).json()
    current_temp = round(response["current_weather"]["temperature"])
    status_code = response["current_weather"]["weathercode"]
    status = WEATHER_STATUS_CODES.get(status_code, f"status #{status_code}")

    lines = [f"{current_temp}° {status}"]

    for i in range(3):
        day_name = RELATIVE_DAY_NAMES[i]
        temp_min = round(response['daily']['temperature_2m_min'][i])
        temp_max = round(response['daily']['temperature_2m_max'][i])
        lines.append(f"{day_name}: {temp_max}°/{temp_min}°")

    return lines
