from playwright.sync_api import sync_playwright
import pandas as pd
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# =========================================================
# GOOGLE SHEET URL
# =========================================================

weekly_schedule_sheet_url = (
    "https://docs.google.com/spreadsheets/d/"
    "1VELKyZUCr_THDbI8zBu_rAAOuIbvP-M344OWCTT4yRA/"
    "export?format=csv&gid=0"
)

config_sheet_url = (
    "https://docs.google.com/spreadsheets/d/"
    "1IhfXHF8s-ZYk-rGmD1Cl2I0hf5Fe1R1_f9Uz5IeCnJ8/"
    "export?format=csv&gid=0"
)

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

USERNAME = os.getenv("TTCH_USERNAME")
PASSWORD = os.getenv("TTCH_PASSWORD")

if not USERNAME or not PASSWORD:
    print("❌ Thiếu TTCH_USERNAME hoặc TTCH_PASSWORD")
    sys.exit()

# =========================================================
# ĐỌC LỊCH TRỰC
# =========================================================

print("🔄 Đang đọc lịch trực...")

df = pd.read_csv(
    weekly_schedule_sheet_url,
    encoding="utf-8-sig"
)

df["ngay"] = pd.to_datetime(
    df["ngay"],
    dayfirst=True,
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

today_rows = df[
    df["ngay"].dt.normalize() == today
]

if today_rows.empty:
    print("❌ Không có lịch trực hôm nay")
    sys.exit()

row = today_rows.iloc[0]

chi_huy_1 = str(row.get("chi_huy_1", "")).strip()
chi_huy_2 = str(row.get("chi_huy_2", "")).strip()

tong_cbcs = str(row.get("tong_cbcs", ""))
cbcs_truc = str(row.get("cbcs_truc", ""))

print("✅ Đọc lịch trực thành công")

# =========================================================
# ĐỌC CONFIG
# =========================================================

print("🔄 Đang đọc config...")

config = pd.read_csv(
    config_sheet_url,
    encoding="utf-8-sig"
)

config_dict = dict(
    zip(config["field"], config["value"])
)

print("✅ Đọc config thành công")

# =========================================================
# FIELD MAPPING
# =========================================================

FIELD_MAPPING = {

    "tong_cbcs":
        'input[placeholder="Nhập tổng số CBCS"]',

    "cbcs_truc":
        'input[placeholder="Nhập số CBCS trực"]',

    "tong_phuong_tien":
        'input[placeholder="Nhập tổng số phương tiện"]',

    "so_phuong_tien_hoat_dong":
        'input[placeholder="Nhập số phương tiện hoạt động"]',

    # "so_phuong_tien_truc":
    #     'input[value="0"]',

    "xe_chua_chay":
        'input[placeholder="Nhập số lượng xe chữa cháy"]',

    "xe_thang":
        'input[placeholder="Nhập số lượng xe thang"]',

    "xe_cuu_nan_cuu_ho":
        'input[placeholder="Nhập số lượng xe cứu nạn, cứu hộ"]',

    "xe_tram_bom":
        'input[placeholder="Nhập số lượng xe trạm bơm"]',

    "xe_cho_nuoc":
        'input[placeholder="Nhập số lượng xe chở nước"]',

    "xe_chi_huy_chua_chay_cuu_nan_cuu_ho":
        'input[placeholder*="xe chỉ huy chữa cháy"]',

    "xe_cho_phuong_tien":
        'input[placeholder="Nhập số lượng xe chở phương tiện"]',

    "xe_cho_quan":
        'input[placeholder="Nhập số lượng xe chở quân"]',

    "xe_hut_khoi":
        'input[placeholder="Nhập số lượng xe hút khói"]',

    "xe_cuu_thuong":
        'input[placeholder="Nhập số lượng xe cứu thương"]',

    "xe_trung_tam_thong_tin_chi_huy":
        'input[placeholder*="xe trung tâm thông tin chỉ huy"]',

    "mo_to_chua_chay_cuu_ho_cuu_thuong":
        'input[placeholder*="mô tô chữa cháy"]',

    "tau_chua_chay":
        'input[placeholder="Nhập số lượng tàu chữa cháy"]',

    "cano_chua_chay_cuu_nan_cuu_ho":
        'input[placeholder*="canô chữa cháy"]',

    "xuong_cuu_nan_cuu_ho_co_dong_co":
        'input[placeholder*="xuồng cứu nạn"]',

    "mo_to_nuoc":
        'input[placeholder*="mô tô nước"]',

    "may_bom_chua_chay_khieng_tay":
        'input[placeholder*="máy bơm chữa cháy"]',

    "may_bom_noi_chua_chay":
        'input[placeholder*="máy bơm nổi chữa cháy"]',

    "robot_chua_chay_cuu_nan_cuu_ho":
        'input[placeholder*="robot chữa cháy"]',

    "phuong_tien_bay_khong_nguoi_lai":
        'input[placeholder*="phương tiện bay không người lái"]',

    "may_nap_khi_sach":
        'input[placeholder*="máy nạp khí sạch"]',

    "chat_tao_bot_chua_chay_thong_thuong":
        'input[placeholder*="chất tạo bọt chữa cháy thông thường"]',

    "chat_tao_bot_chua_chay_cong_nghe_cafs":
        'input[placeholder*="công nghệ CAFS"]',

    "chat_tao_bot_chua_chay_cong_nghe_1_7":
        'input[placeholder*="công nghệ 1-7"]',

    "mat_na_phong_doc_cach_ly":
        'input[placeholder*="mặt nạ phòng độc"]',

    "bo_dam_cam_tay_vhf_uhf":
    'input[placeholder*="VHF/UHF"]',

    "ghi_chu":
    'input[placeholder="Nhập ghi chú"]'
}

# =========================================================
# PLAYWRIGHT
# =========================================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=1000,
        args=["--start-maximized"]
    )

    context = browser.new_context(
        viewport=None
    )

    page = context.new_page()

    page.set_default_timeout(30000)

    # =====================================================
    # HELPER
    # =====================================================

    def safe_click(locator, retry=3):

        for i in range(retry):

            try:

                locator.wait_for(
                    state="visible",
                    timeout=15000
                )

                locator.scroll_into_view_if_needed()

                page.wait_for_timeout(1000)

                locator.click(force=True)

                return

            except Exception as e:

                print(f"⚠️ Retry click {i+1}")

                page.wait_for_timeout(2000)

        raise Exception("❌ Click failed")

    def safe_fill(locator, value):

        locator.wait_for(
            state="visible",
            timeout=15000
        )

        locator.scroll_into_view_if_needed()

        locator.fill(str(value))

    # =====================================================
    # LOGIN
    # =====================================================

    print("🔄 Đang mở website...")

    page.goto(
        "https://ttch.csdlcbcs.vn",
        wait_until="domcontentloaded"
    )

    page.wait_for_load_state("networkidle")

    username_input = page.locator(
        'input[placeholder="Nhập tên đăng nhập của bạn"]'
    )

    password_input = page.locator(
        'input[placeholder="Nhập mật khẩu của bạn"]'
    )

    safe_fill(username_input, USERNAME)
    safe_fill(password_input, PASSWORD)

    print("🔄 Đang đăng nhập...")

    login_button = page.locator(
        'button:has-text("Đăng nhập")'
    )

    safe_click(login_button)

    page.wait_for_load_state("networkidle")

    print("✅ Đăng nhập thành công")

    # =====================================================
    # CHỌN TTCH
    # =====================================================

    print("🔄 Đang chọn TTCH...")

    ttch_button = page.locator(
        'div.shadow-md.rounded-xl'
    ).nth(1)

    safe_click(ttch_button)

    page.wait_for_load_state("networkidle")

    print("✅ Đã chọn TTCH")

    # =====================================================
    # QUẢN TRỊ
    # =====================================================
    # đợi tab Quản trị xuất hiện
    page.wait_for_selector(
    "text=Quản trị",
    timeout=15000
    )

    print("🔄 Đang mở Quản trị...")

    quan_tri_button = page.locator(
        "text=Quản trị"
    ).first

    safe_click(quan_tri_button)

    page.wait_for_load_state("networkidle")

    print("✅ Đã mở Quản trị")

    # =====================================================
    # LỊCH TRỰC
    # =====================================================

    print("🔄 Đang mở lịch trực...")
    # đợi menu lịch trực xuất hiện
    page.wait_for_selector(
        "text=Lịch trực sẵn sàng chữa cháy, cứu nạn, cứu hộ",
        timeout=15000
    )

    lich_truc_button = page.locator(
        "text=Lịch trực sẵn sàng chữa cháy, cứu nạn, cứu hộ"
    ).first

    safe_click(lich_truc_button)

    page.wait_for_load_state("networkidle")

    print("✅ Đã mở lịch trực")


    # =====================================================
    # KIỂM TRA HÔM NAY ĐÃ NHẬP LỊCH TRỰC
    # =====================================================

    today_text = datetime.now().strftime("%d/%m/%Y")

    print(f"🔄 Kiểm tra lịch trực ngày {today_text}...")

    page.wait_for_timeout(3000)

    # tìm record có chứa ngày hôm nay
    today_record = page.locator(
        f'tr:has-text("{today_text}")'
    )

    # chỉ cần >= 1 record
    if today_record.count() >= 1:

        print("⚠️ Lịch trực hôm nay đã tồn tại")

        page.screenshot(
            path="lich_truc_hom_nay_da_ton_tai.png",
            full_page=True
        )

        print("📸 Đã chụp màn hình")
        print("✅ Đã có lịch trực hôm nay")

        input("Nhấn Enter để đóng browser...")

        browser.close()

        sys.exit()

    print("✅ Chưa có lịch trực hôm nay")

    # =====================================================
    # THÊM MỚI
    # =====================================================

    print("🔄 Đang mở form thêm mới...")

    them_moi_button = page.locator(
        "text=Thêm mới"
    ).first

    safe_click(them_moi_button)

    page.wait_for_selector(
        '.ant-modal-content',
        state="visible"
    )

    print("✅ Đã mở form thêm mới")

   
    # =====================================================
    # FILL FORM
    # =====================================================

    print("🔄 Đang fill form...")

    form_data = {
        "tong_cbcs": tong_cbcs,
        "cbcs_truc": cbcs_truc
    }

    form_data.update(config_dict)

    for field_name, selector in FIELD_MAPPING.items():

        value = form_data.get(field_name)

        if value is None:
            continue

        if pd.isna(value) or str(value).strip() == "":
            continue

        try:

            locator = page.locator(selector).first

            safe_fill(locator, value)

            print(f"✅ {field_name}: {value}")

        except Exception as e:

            print(f"❌ Lỗi field: {field_name}")
            print(e)
    

# # =====================================================
# # CHỌN CHỈ HUY
# # =====================================================

# print("🔄 Đang chọn chỉ huy trực...")

# chi_huy_dropdown = page.locator(
#     'input[placeholder="Chọn chỉ huy trực"]'
# ).first

# chi_huy_dropdown.wait_for(state="visible")

# chi_huy_dropdown.click()

# page.wait_for_timeout(1000)

# if chi_huy_1 == "Nguyễn Thành Tuân":

#     page.locator(
#         "text=Nguyễn Thành Tuân"
#     ).click()

#     print("✅ Đã chọn Nguyễn Thành Tuân")

# else:

#     page.locator(
#         "text=Khác"
#     ).click()

#     page.wait_for_timeout(1000)

#     page.locator(
#         'input[placeholder="Nhập họ tên chỉ huy trực"]'
#     ).fill("Lê Văn Dũng")

#     page.locator(
#         'input[placeholder="Nhập số điện thoại chỉ huy trực"]'
#     ).fill("0384319203")

#     print("✅ Đã nhập chỉ huy ngoài danh sách")


    # =====================================================
    # SCREENSHOT
    # =====================================================

    page.screenshot(path="08_final.png")

    print("✅ Hoàn thành")

    input("Nhấn Enter để đóng browser...")

    browser.close()