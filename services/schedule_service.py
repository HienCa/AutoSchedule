import os
import json
import gspread
from google.oauth2.service_account import Credentials

from datetime import datetime

from config.settings import (
    WEEKLY_SHEET_URL
)

def open_schedule_page(page):

    print("🔄 Đang chọn TTCH...")

    ttch_button = page.locator(
        'div.shadow-md.rounded-xl'
    ).nth(1)

    ttch_button.wait_for(state="visible")

    ttch_button.click(force=True)

    page.wait_for_load_state("networkidle")

    print("✅ Đã chọn TTCH")

    # ==================================================
    # QUẢN TRỊ
    # ==================================================

    print("🔄 Đang mở Quản trị...")

    page.wait_for_selector(
        "text=Quản trị",
        timeout=30000
    )

    quan_tri_button = page.locator(
        "text=Quản trị"
    ).first

    quan_tri_button.click(force=True)

    page.wait_for_load_state("networkidle")

    print("✅ Đã mở Quản trị")

    # ==================================================
    # LỊCH TRỰC
    # ==================================================

    print("🔄 Đang mở lịch trực...")

    page.wait_for_selector(
        "text=Lịch trực sẵn sàng chữa cháy, cứu nạn, cứu hộ",
        timeout=30000
    )

    lich_truc_button = page.locator(
        "text=Lịch trực sẵn sàng chữa cháy, cứu nạn, cứu hộ"
    ).first

    lich_truc_button.click(force=True)

    page.wait_for_load_state("networkidle")

    print("✅ Đã mở lịch trực")


def check_schedule_exists(page):

    # check ngày mai
    # tomorrow = datetime.now() + timedelta(days=1)

    today_text = datetime.now().strftime("%d/%m/%Y")

    print(f"🔍 Đang check lịch trực ngày: {today_text}")

    # đợi table load
    page.wait_for_timeout(5000)

    # debug screenshot
    page.screenshot(
        path="screenshots/check_schedule.png",
        full_page=True
    )

    rows = page.locator("tr")

    count = rows.count()

    print(f"📋 Tổng số rows: {count}")

    for i in range(count):

        try:

            row_text = rows.nth(i).inner_text()

            # print(f"ROW {i}: {row_text}")

            if today_text in row_text:

                print("⚠️ Đã tồn tại lịch trực")

                return True

        except:
            pass

    print("✅ Chưa có lịch trực")

    return False

import os
import json
import gspread

from google.oauth2.service_account import Credentials

from config.settings import WEEKLY_SHEET_URL


def get_gsheet():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # =========================================
    # SERVER / CLOUD
    # =========================================

    google_credentials = os.getenv("GOOGLE_CREDENTIALS")

    if google_credentials:

        creds_dict = json.loads(google_credentials)

        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=scope
        )

    # =========================================
    # LOCAL
    # =========================================

    else:

        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )

    client = gspread.authorize(creds)

    return client.open_by_url(
        WEEKLY_SHEET_URL
    ).sheet1

def get_trang_thai():
    """Đọc trạng thái ON/OFF từ 1 ô trong sheet."""
    sheet = get_gsheet()
    # Ô B1 chứa trạng thái
    trang_thai = sheet.acell('G2').value
    return str(trang_thai).strip().upper()

def set_trang_thai( value: str):
    """Cập nhật trạng thái ON/OFF."""
    sheet = get_gsheet()
    sheet.update_acell('G2', value)
    print(f"✅ Trạng thái → {value}")