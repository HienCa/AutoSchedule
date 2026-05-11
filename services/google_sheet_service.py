import pandas as pd

from config.settings import (
    WEEKLY_SHEET_URL,
    CONFIG_SHEET_URL
)

def get_today_schedule():

    df = pd.read_csv(
        WEEKLY_SHEET_URL,
        encoding="utf-8-sig"
    )

    df["ngay"] = pd.to_datetime(
        df["ngay"],
        dayfirst=True,
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    row = df[
        df["ngay"].dt.normalize() == today
    ].iloc[0]

    return row.to_dict()


def get_config():

    config = pd.read_csv(
        CONFIG_SHEET_URL,
        encoding="utf-8-sig"
    )

    return dict(
        zip(
            config["field"],
            config["value"]
        )
    )