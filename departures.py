from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

TIMEZONE = ZoneInfo("Europe/Warsaw")


# departures.csv should be a file like:
# route,day,hour,minute
# 158,0,4,43
# 158,0,5,13
# 158,0,5,33

def get_departures() -> list[str]:
    now = datetime.now(TIMEZONE)
    current_minutes_since_week_start = (24 * now.weekday() + now.hour) * 60 + now.minute

    df = pd.read_csv("departures.csv")
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
