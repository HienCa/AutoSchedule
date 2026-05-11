from datetime import datetime, timedelta
import sys


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
        timeout=20000
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
        timeout=20000
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