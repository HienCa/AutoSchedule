import pandas as pd
import datetime

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

def get_today_schedule():
    df = pd.read_csv(
        WEEKLY_SHEET_URL,
        encoding="utf-8-sig",
        dtype={"phone": str, "tong_cbcs": str, "cbcs_truc": str}  # Ép tất cả cột dạng số thành str
    )
    
    today_name = datetime.datetime.now().strftime("%A")
    today_row = df[df['ngay'] == today_name]
    
    if today_row.empty:
        raise Exception(f"Không tìm thấy lịch trực cho thứ: {today_name}")
        
    row = today_row.iloc[0]

    # Xử lý phone sạch
    phone_raw = str(row.get('phone', '')).strip()
    phone = "" if phone_raw in ("nan", "None", "") else phone_raw

    return {
        "chi_huy": str(row['chi_huy']).strip(),
        "phone":     phone,
        "tong_cbcs": str(row['tong_cbcs']).strip(),
        "cbcs_truc": str(row['cbcs_truc']).strip()
    }
