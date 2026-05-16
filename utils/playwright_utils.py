def safe_click(page, locator, retry=3):

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

        except Exception:

            print(f"⚠️ Retry click {i+1}")

            page.wait_for_timeout(2000)

    raise Exception("❌ Click failed")


def safe_fill(page, locator, value):

    locator.wait_for(
        state="visible",
        timeout=30000
    )

    locator.scroll_into_view_if_needed()

    locator.fill(str(value))

