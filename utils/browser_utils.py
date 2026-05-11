def create_browser(p):

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

    return browser, page