import pickle
from pathlib import Path
from typing import Optional

from google.auth.external_account_authorized_user import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

TOKENS_PATH = "tokens.pickle"
SECRET_PATH = "secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


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


def get_events() -> list[str]:
    return ["10:15 TKOM", "", "", "", "", "", "", "", "", "", "", ""]
