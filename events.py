import pickle
from datetime import datetime
from pathlib import Path
from typing import Optional

from google.auth.external_account_authorized_user import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

TOKENS_PATH = "tokens.pickle"
SECRET_PATH = "secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

LINE_COUNT = 9
LINE_WIDTH = 18

TIMEZONE_OFFSET = "+01:00"


def load_tokens() -> Optional[Credentials]:
    if not Path(TOKENS_PATH).is_file():
        return None
    with open(TOKENS_PATH, "rb") as file:
        tokens = pickle.load(file)
    if not tokens.valid:
        tokens.refresh(Request())
    return tokens


def create_tokens() -> Credentials:
    if not Path(SECRET_PATH).is_file():
        raise FileNotFoundError(SECRET_PATH)
    flow = InstalledAppFlow.from_client_secrets_file(SECRET_PATH, SCOPES)
    tokens = flow.run_local_server(port=0)
    with open(TOKENS_PATH, "wb") as file:
        pickle.dump(tokens, file)
    return tokens


def get_tokens() -> Credentials:
    loaded = load_tokens()
    if loaded:
        return loaded
    return create_tokens()


def get_calendar_ids(service: Resource) -> list[str]:
    return [item["id"] for item in service.calendarList().list().execute()["items"]]


def format_event(event: dict) -> str:
    if "dateTime" in event["start"]:
        start_time = event["start"]["dateTime"][11:16]
    else:
        start_time = event["start"]["date"][5:10]

    name = event["summary"]
    if len(name) > LINE_WIDTH - 6:
        name = name[:LINE_WIDTH - 7] + "…"

    return f"{start_time} {name}"


def get_json_events(service: Resource, calendar_id: str) -> list[dict]:
    now = datetime.utcnow()
    next_midnight = now.replace(hour=23, minute=59, second=59)
    return service.events().list(
        calendarId=calendar_id,
        timeMin=now.isoformat() + TIMEZONE_OFFSET,
        timeMax=next_midnight.isoformat() + TIMEZONE_OFFSET,
        maxResults=LINE_COUNT,
        singleEvents=True,
        orderBy="startTime",
    ).execute()["items"]


def get_event_lines() -> list[str]:
    tokens = get_tokens()
    service = build("calendar", "v3", credentials=tokens)
    calendar_ids = get_calendar_ids(service)
    events = []
    for calendar_id in calendar_ids:
        events.extend(get_json_events(service, calendar_id))
    lines = [format_event(json) for json in events[:LINE_COUNT]]
    if len(lines) < LINE_COUNT:
        lines.extend((LINE_COUNT - len(lines)) * [""])
    return lines


def main():
    print(get_event_lines())


if __name__ == '__main__':
    main()
