def create_browser(p):
    browser = p.chromium.launch(
        headless=False,
        slow_mo=1000,
        args=[
            # "--start-maximized",
            # "--disable-infobars",
            # "--no-sandbox"
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",  # Quan trọng trên Linux
            "--disable-gpu",
            "--single-process"
        ]
    )

    context = browser.new_context(
        no_viewport=True  # Dùng kích thước thật của cửa sổ
    )

    page = context.new_page()
    page.set_default_timeout(60000)

    # Maximize qua CDP
    session = context.new_cdp_session(page)
    session.send("Browser.getWindowForTarget")
    window_id = session.send("Browser.getWindowForTarget")["windowId"]
    session.send("Browser.setWindowBounds", {
        "windowId": window_id,
        "bounds": {"windowState": "maximized"}
    })

    return browser, page