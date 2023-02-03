from datetime import datetime

from flask import Flask, request, Response

from buses import get_buses
from events import get_events
from weather import get_weather

VOLTAGE_LOG_PATH = "/home/szw/lilygo/voltage.log"

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
        events=get_events(),
        buses=get_buses(),
        weather=get_weather(),
        time=datetime.now().strftime("%H:%M")
    )

    # if message is same as before, respond with 304 Not Modified
    etag = hash(message)
    if request.headers.get('If-None-Match') == str(etag):
        return Response(status=304)

    # otherwise, respond 200 OK and the message
    return Response(response=message, status=200, headers={'ETag': etag})
