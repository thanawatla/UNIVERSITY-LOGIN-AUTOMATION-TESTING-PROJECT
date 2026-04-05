from playwright.sync_api import sync_playwright

# ✅ PASS: Login success (ถูกต้อง)
def test_login_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        assert page.url == "https://www.saucedemo.com/inventory.html"

        browser.close()


# ❌ FAIL: Login success แต่ assert ผิด 
def test_login_success_wrong_assert():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")

        # ❌ ตั้งใจเช็คว่าไป URL นี้ไหม
        assert page.url == "https://www.saucedemo.com/dashboard"

        browser.close()


# ✅ PASS: Login fail (เช็คข้อความถูกต้อง)
def test_login_fail_correct():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", "wrong_user")
        page.fill("#password", "wrong_pass")
        page.click("#login-button")

        error = page.locator(".error-message-container")
        assert "Username and password do not match" in error.inner_text()

        browser.close()


# ❌ FAIL: Login fail แต่ assert ข้อความผิด
def test_login_fail_wrong_message():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", "wrong_user")
        page.fill("#password", "wrong_pass")
        page.click("#login-button")

        error = page.locator(".error-message-container")

        # ❌ ตั้งใจเช็คข้อความผิด
        assert "Login successful" in error.inner_text()

        browser.close()


