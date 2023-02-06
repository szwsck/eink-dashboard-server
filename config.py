VOLTAGE_LOG_PATH = "/home/szw/lilygo/voltage.log"
TEMPLATE_PATH = "template.txt"

# should match sizes in template.txt
SECTION_SIZES = {
    "events": (4, 38),
    "departures": (4, 16),
    "weather": (4, 19)
}

# secrets.json should contain API keys from Google Developer Console
SECRET_PATH = "secret.json"
TOKENS_PATH = "tokens.pickle"
TIMEZONE = "Europe/Warsaw"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# departures.csv should be a file like:
# route,day,hour,minute
# 158,0,4,43
# 158,0,5,13
# 158,0,5,33
DEPARTURES_PATH = "departures.csv"

# https://open-meteo.com/en/docs
WEATHER_URL = "https://api.open-meteo.com/v1/forecast" \
              "?latitude=52.23&longitude=21.00" \
              "&timezone=auto" \
              "&current_weather=true" \
              "&daily=temperature_2m_min,temperature_2m_max"
WEATHER_STATUS_CODES = {
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
RELATIVE_DAY_NAMES = ["Dziś", "Jutro", "Pojutrze"]
