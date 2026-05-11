from playwright.sync_api import sync_playwright
import traceback
import os

from services.google_sheet_service import (
    get_today_schedule,
    get_config
)

from services.auth_service import login

from services.schedule_service import (
    open_schedule_page,
    check_schedule_exists
)

from services.form_service import (
    open_create_form,
    fill_schedule_form
)

from services.telegram_service import (
    send_telegram_message,
    send_telegram_photo
)

from utils.browser_utils import create_browser


# ==================================================
# HELPER
# ==================================================

def ensure_screenshot_folder():

    os.makedirs(
        "screenshots",
        exist_ok=True
    )


# ==================================================
# MAIN
# ==================================================

print("==================================================")
print("🚀 BẮT ĐẦU CHẠY AUTOSCHEDULE")
print("==================================================")


try:

    # ==================================================
    # ĐỌC GOOGLE SHEET
    # ==================================================

    print("🔄 Đang đọc lịch trực hôm nay...")

    schedule_data = get_today_schedule()

    print("✅ Đọc lịch trực thành công")

    print("--------------------------------------------------")

    print("📋 THÔNG TIN LỊCH TRỰC")

    for key, value in schedule_data.items():

        print(f"{key}: {value}")

    print("--------------------------------------------------")

    print("🔄 Đang đọc config...")

    config_data = get_config()

    print("✅ Đọc config thành công")

    print("--------------------------------------------------")

    print("📋 THÔNG TIN CONFIG")

    for key, value in config_data.items():

        print(f"{key}: {value}")

    print("--------------------------------------------------")

    # ==================================================
    # PLAYWRIGHT
    # ==================================================

    with sync_playwright() as p:

        print("🌐 Đang mở browser...")

        browser, page = create_browser(p)

        print("✅ Browser đã mở")

        # ==================================================
        # LOGIN
        # ==================================================

        print("==================================================")
        print("🔐 ĐANG ĐĂNG NHẬP")
        print("==================================================")

        login(page)

        print("✅ Đăng nhập thành công")

        # ==================================================
        # MỞ LỊCH TRỰC
        # ==================================================

        print("==================================================")
        print("📂 ĐANG MỞ TRANG LỊCH TRỰC")
        print("==================================================")

        open_schedule_page(page)

        print("✅ Đã mở trang lịch trực")

        # ==================================================
        # CHECK ĐÃ TỒN TẠI
        # ==================================================

        print("==================================================")
        print("🔍 KIỂM TRA LỊCH TRỰC HÔM NAY")
        print("==================================================")

        # exists = check_schedule_exists(page)

        # # ==================================================
        # # ĐÃ TỒN TẠI
        # # ==================================================

        # if exists:

        #     print("⚠️ LỊCH TRỰC HÔM NAY ĐÃ TỒN TẠI")

        #     ensure_screenshot_folder()

        #     existed_image = (
        #         "screenshots/existed.png"
        #     )

        #     page.screenshot(
        #         path=existed_image,
        #         full_page=True
        #     )

        #     print(
        #         f"📸 Đã chụp màn hình: {existed_image}"
        #     )

        #     # ==========================================
        #     # TELEGRAM
        #     # ==========================================

        #     print("📨 Đang gửi Telegram...")

        #     send_telegram_message(
        #         "⚠️ Lịch trực hôm nay đã tồn tại"
        #     )

        #     send_telegram_photo(
        #         existed_image,
        #         caption=(
        #             "📸 Lịch trực hôm nay "
        #             "đã tồn tại trên hệ thống"
        #         )
        #     )

        #     print("✅ Đã gửi Telegram")

        #     print("==================================================")
        #     print("⛔ KẾT THÚC")
        #     print("==================================================")

        #     browser.close()

        #     exit()

        # print("✅ Chưa có lịch trực hôm nay")

        # ==================================================
        # MỞ FORM
        # ==================================================

        print("==================================================")
        print("📝 ĐANG MỞ FORM THÊM MỚI")
        print("==================================================")

        open_create_form(page)

        print("✅ Đã mở form thêm mới")

        # ==================================================
        # FILL FORM
        # ==================================================

        print("==================================================")
        print("✍️ ĐANG FILL FORM")
        print("==================================================")

        fill_schedule_form(
            page,
            schedule_data,
            config_data
        )

        print("✅ Fill form thành công")

        # ==================================================
        # SCREENSHOT
        # ==================================================

        print("📸 Đang chụp màn hình kết quả...")

        ensure_screenshot_folder()

        done_image = (
            "screenshots/done.png"
        )

        page.screenshot(
            path=done_image,
            full_page=True
        )

        print(
            f"✅ Đã lưu screenshot: {done_image}"
        )

        # ==================================================
        # TELEGRAM
        # ==================================================

        print("📨 Đang gửi Telegram...")

        send_telegram_message(
            "✅ Đã nhập lịch trực thành công"
        )

        send_telegram_photo(
            done_image,
            caption=(
                "📸 Đã nhập lịch trực "
                "thành công"
            )
        )

        print("✅ Đã gửi Telegram")

        print("==================================================")
        print("🎉 HOÀN THÀNH AUTOSCHEDULE")
        print("==================================================")

        browser.close()

# =========================================================
# ERROR
# =========================================================

except Exception as e:

    print("==================================================")
    print("❌ CÓ LỖI XẢY RA")
    print("==================================================")

    print(str(e))

    traceback_error = traceback.format_exc()

    print(traceback_error)

    try:

        send_telegram_message(
            "❌ AutoSchedule gặp lỗi\n\n"
            f"{str(e)}"
        )

    except Exception as tele_error:

        print("❌ Không gửi được Telegram")

        print(tele_error)