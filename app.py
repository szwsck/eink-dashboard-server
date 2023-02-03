from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, request, Response

from buses import get_bus_lines
from events import get_event_lines
from weather import get_weather_lines

VOLTAGE_LOG_PATH = "/home/szw/lilygo/voltage.log"
TIMEZONE = ZoneInfo("Europe/Warsaw")

app = Flask(__name__)


def log_voltage():
    # retrieve and log voltage
    voltage = request.args.get("voltage", default="")
    with open(VOLTAGE_LOG_PATH, 'a') as log_file:
        log_file.write(f"{datetime.now().isoformat()},{voltage}\n")


@app.get("/lilygo")
def lilygo():
    log_voltage()

    # construct message
    with open("template.txt", "r") as template_file:
        template = template_file.read()
    message = template.format(
        events=get_event_lines(),
        buses=get_bus_lines(),
        weather=get_weather_lines(),
        time=datetime.now(TIMEZONE).strftime("%H:%M")
    )

    # if message is same as before, respond with 304 Not Modified
    etag = hash(message)
    if request.headers.get('If-None-Match') == str(etag):
        return Response(status=304)

    # otherwise, respond 200 OK and the message
    return Response(response=message, status=200, headers={'ETag': etag})
