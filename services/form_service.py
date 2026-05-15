import pandas as pd

from config.field_mapping import FIELD_MAPPING

from utils.playwright_utils import (
    safe_click,
    safe_fill
)

def open_create_form(page):

    button = page.locator(
        "text=Thêm mới"
    ).first

    safe_click(page, button)


import pandas as pd

def fill_schedule_form(page, schedule_data, config_data):
    # Gộp dữ liệu từ Sheet và Config
    form_data = {**schedule_data, **config_data}
    
    # 1. XỬ LÝ RIÊNG CHO MỤC CHỈ HUY (DROPDOWN)
    ten_chi_huy = schedule_data.get("chi_huy", "").strip()
    phone_chi_huy = schedule_data.get("phone", "").strip()

    print(f"🔄 Đang xử lý chỉ huy: {ten_chi_huy}")

    try:
        # Locate đúng wrapper chứa placeholder "Chọn chỉ huy trực"
        selector_wrapper = page.locator(
            '.ant-select-selector:has(.ant-select-selection-placeholder:text-is("Chọn chỉ huy trực"))'
        )
        selector_wrapper.wait_for(state="visible", timeout=10000)
        selector_wrapper.click()
        page.wait_for_timeout(400)

        # Input search nằm bên trong wrapper vừa click
        search_input = selector_wrapper.locator('input.ant-select-selection-search-input')
        search_input.wait_for(state="visible", timeout=5000)

        # Fill tên để trigger dropdown list hiện ra
        search_input.fill(ten_chi_huy)
        page.wait_for_timeout(500)  # Chờ list render

        # Lấy options SAU KHI đã fill (dropdown đã mở)
        # Lấy text của phần tên (element đầu tiên trong mỗi option)
        option_items = page.locator('.ant-select-item-option-content').all()

        available_options = []
        for item in option_items:
            # Lấy dòng đầu tiên (tên), bỏ phần chức vụ/phone bên dưới
            full_text = item.inner_text().strip()
            name_only = full_text.split('\n')[0].strip()
            available_options.append(name_only)

        print(f"📋 Options có sẵn: {available_options}")

        if ten_chi_huy in available_options:
            # Tên khớp → click trực tiếp
            page.locator('.ant-select-item-option-content').filter(
                has_text=ten_chi_huy
            ).first.click()
            print(f"✅ Đã chọn: {ten_chi_huy}")

        else:
            # Không có → xóa, tìm "Khác"
            search_input.fill("Khác")
            page.wait_for_timeout(400)
            page.locator('.ant-select-item-option-content').filter(
                has_text="Khác"
            ).first.click()
            page.wait_for_timeout(500)

            name_input = page.locator('input[placeholder="Nhập họ tên chỉ huy trực"]').first
            name_input.wait_for(state="visible", timeout=5000)
            safe_fill(page, name_input, ten_chi_huy)

            if phone_chi_huy:
                phone_input = page.locator('input[placeholder="Nhập số điện thoại chỉ huy trực"]').first
                phone_input.wait_for(state="visible", timeout=5000)
                safe_fill(page, phone_input, phone_chi_huy)

            print(f"✅ Đã nhập thủ công: {ten_chi_huy}")

    except Exception as e:
        print(f"❌ Lỗi khi chọn chỉ huy: {e}")

    # 2. XỬ LÝ CÁC FIELD CÒN LẠI QUA VÒNG LẶP (SỬ DỤNG SAFE_FILL)
    FIELDS_TO_SKIP = ["chi_huy", "phone"]

    for field_name, selector in FIELD_MAPPING.items():
        if field_name in FIELDS_TO_SKIP:
            continue

        value = form_data.get(field_name)

        # Kiểm tra giá trị hợp lệ
        if value is None or (isinstance(value, float) and pd.isna(value)) or str(value).strip() == "":
            continue

        try:
            locator = page.locator(selector).first
            
            # GỌI SAFE_FILL CỦA BẠN TẠI ĐÂY
            safe_fill(page, locator, value)
            
            print(f"✅ {field_name}: {value}")

        except Exception as e:
            print(f"❌ Lỗi field: {field_name}")
            print(f"Chi tiết: {e}")
    
    submit_schedule(page)


def submit_schedule(page):

    print("🔄 Đang lưu lịch trực...")

    try:

        # ưu tiên tìm theo id
        submit_button = page.locator(
            '#online-calendar-create_button'
        )

        submit_button.wait_for(
            state="visible",
            timeout=5000
        )

    except:

        print("⚠️ Không tìm thấy button bằng id")
        print("🔄 Chuyển sang tìm theo text...")

        submit_button = page.locator(
            'button:has-text("Thêm mới")'
        ).last

    safe_click(page, submit_button)

    page.wait_for_load_state("networkidle")

    print("✅ Đã thêm mới lịch trực")