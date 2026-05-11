from config.settings import (
    TTCH_USERNAME,
    TTCH_PASSWORD
)

from utils.playwright_utils import (
    safe_click,
    safe_fill
)

def login(page):

    page.goto("https://ttch.csdlcbcs.vn")

    username_input = page.locator(
        'input[placeholder="Nhập tên đăng nhập của bạn"]'
    )

    password_input = page.locator(
        'input[placeholder="Nhập mật khẩu của bạn"]'
    )

    safe_fill(page, username_input, TTCH_USERNAME)

    safe_fill(page, password_input, TTCH_PASSWORD)

    login_button = page.locator(
        'button:has-text("Đăng nhập")'
    )

    safe_click(page, login_button)

    page.wait_for_load_state("networkidle")