from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

from config import DEPARTURES_PATH, TIMEZONE


def get_departures() -> list[str]:
    now = datetime.now(ZoneInfo(TIMEZONE))
    current_minutes_since_week_start = (24 * now.weekday() + now.hour) * 60 + now.minute

    df = pd.read_csv(DEPARTURES_PATH)
    minutes_since_week_start = (24 * df["day"] + df["hour"]) * 60 + df["minute"]

    df["diff"] = (minutes_since_week_start - current_minutes_since_week_start) % (7 * 24 * 60)
    df.sort_values(by="diff", inplace=True)

    lines = []
    for route, departures in df.groupby("route"):
        line = f"{route}:"
        for row in departures[:2].itertuples():
            line += f" {row.hour:0>2}:{row.minute:0>2}"
        lines.append(line)

    return lines
