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


def fill_schedule_form(
    page,
    schedule_data,
    config_data
):

    form_data = {}

    form_data.update(schedule_data)

    form_data.update(config_data)

    for field_name, selector in FIELD_MAPPING.items():

        value = form_data.get(field_name)

        if value is None:
            continue

        if pd.isna(value):
            continue

        try:

            locator = page.locator(
                selector
            ).first

            safe_fill(
                page,
                locator,
                value
            )

            print(f"✅ {field_name}")

        except Exception as e:

            print(f"❌ {field_name}")
            print(e)