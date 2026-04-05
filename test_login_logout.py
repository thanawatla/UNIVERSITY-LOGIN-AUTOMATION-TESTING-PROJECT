import pytest
from playwright.sync_api import Page, sync_playwright
from test_logger import log_result

# -------------------------- POSITIVE TEST -------------------------- #
""" Positive Test Scenario 01 START """
# กรณีทดสอบ: เข้าสู่ระบบด้วยข้อมูลที่ถูกต้อง ควร redirect ไปยังหน้าเปลี่ยนรหัสผ่าน

def test_login01_pos01():
    with sync_playwright() as p:
        # เปิดเบราว์เซอร์
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ไปยังหน้า Login
        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        # กรอกข้อมูลเข้าสู่ระบบ (ข้อมูลที่ถูกต้อง)
        page.locator('input[name="f_uid"]').fill("65502100044-4")
        page.locator('input[name="f_pwd"]').fill("abc25965")
        page.locator('input[name="f_idcard"]').fill("1103100809111")

        # คลิกปุ่ม "เข้าสู่ระบบ"
        page.locator('input[type="submit"]').click()
        page.wait_for_load_state("networkidle")

        print(f"📌 DEBUG: Current Page URL → {page.url}")

        # ตรวจสอบว่า redirect ไปยังหน้า changepwd หรือไม่
        expected_url_prefix = "https://reg.rmutk.ac.th/registrar/changepwd.asp"
        if page.url.startswith(expected_url_prefix):
            actual_result = "✅ Login successful, redirected to 'Change Password'"
        else:
            actual_result = f"❌ Login successful but redirected to wrong page: {page.url}"

        # บันทึกผลลัพธ์
        log_result("login01_pos01", actual_result, page=page)

        # ตรวจสอบ URL ที่เปลี่ยนไป
        assert page.url.startswith(expected_url_prefix), "❌ Login did not redirect to Change Password page!"

        browser.close()

""" Positive Test Scenario 01 END """
# -------------------------- END POSITIVE TEST -------------------------- #


# -------------------------- NEGATIVE TEST -------------------------- #
# ฟังก์ชันช่วยตรวจสอบว่าสีเป็นสีน้ำเงินหรือไม่
def is_blue(rgb_string):
    rgb_values = [int(x) for x in rgb_string.replace("rgb(", "").replace(")", "").split(",")]
    r, g, b = rgb_values
    return r < 30 and g < 30 and b > 200

# ฟังก์ชันช่วยตรวจสอบว่าสีเป็นสีแดงหรือไม่
def is_red(rgb_string):
    rgb_values = [int(x) for x in rgb_string.replace("rgb(", "").replace(")", "").split(",")]
    r, g, b = rgb_values
    return r > 200 and g < 50 and b < 50


""" Negative Test Scenario 01 START """
# กรณีทดสอบ: ล็อกอินด้วยรหัสและรหัสบัตรประชาชน ผิด ควรแสดงข้อความแจ้งเตือนสีน้ำเงิน

def test_login01_neg01():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        # กรอกข้อมูลผิด
        page.locator('input[name="f_uid"]').fill("65502100044-4")
        page.locator('input[name="f_pwd"]').fill("55555")
        page.locator('input[name="f_idcard"]').fill("5555")

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            # ตรวจสอบว่ามีข้อความแจ้งเตือนหรือไม่
            error_element = page.locator(
                "xpath=//font[contains(text(),'ก รุ ณ า ป้ อ น ร หั ส ป ร ะ จ ำ ตั ว น ศ .ร หั ส บั ต ร ป ร ะ ช า ช น แ ล ะ ร หั ส ผ่ า น ใ ห้ ถู ก ต้ อ ง')]"
            ).first
            assert error_element.is_visible()

            # ตรวจสอบสีข้อความ
            color = error_element.evaluate("el => window.getComputedStyle(el).color")
            print(f"📌 DEBUG: สีของข้อความแจ้งเตือน → {color}")

            if is_blue(color):
                actual_result = "✅ พบข้อความแจ้งเตือน และเป็นสีน้ำเงิน"
                status = "PASS"
            else:
                actual_result = "❌ พบข้อความแจ้งเตือน แต่เป็นสีแดง"
                status = "FAIL"

        except Exception:
            actual_result = "❌ ไม่พบข้อความแจ้งเตือน"
            status = "FAIL"

        log_result("login01_neg01", actual_result, page=page)
        assert status == "PASS", "❌ ข้อความไม่พบ หรือ สีไม่ถูกต้อง!"
        browser.close()

""" Negative Test Scenario 01 END """


""" Negative Test Scenario 02 START """
# กรณีทดสอบ: ล็อกอินด้วยรหัสบัตรประชาชนผิด ควรแสดงข้อความแจ้งเตือนสีน้ำเงิน

def test_login01_neg02():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        # กรอกข้อมูลผิด (รหัสบัตรประชาชนผิด)
        page.locator('input[name="f_uid"]').fill("65502100044-4")
        page.locator('input[name="f_pwd"]').fill("abc25965")
        page.locator('input[name="f_idcard"]').fill("5555")

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            error_element = page.locator(
                "xpath=//font[contains(text(),'ก รุ ณ า ป้ อ น ร หั ส ป ร ะ จ ำ ตั ว น ศ .ร หั ส บั ต ร ป ร ะ ช า ช น แ ล ะ ร หั ส ผ่ า น ใ ห้ ถู ก ต้ อ ง')]"
            ).first
            assert error_element.is_visible()

            color = error_element.evaluate("el => window.getComputedStyle(el).color")
            print(f"📌 DEBUG: สีของข้อความแจ้งเตือน → {color}")

            if is_blue(color):
                actual_result = "✅ พบข้อความแจ้งเตือน และเป็นสีน้ำเงิน"
                status = "PASS"
            else:
                actual_result = "❌ พบข้อความแจ้งเตือน แต่เป็นสีแดง"
                status = "FAIL"

        except Exception:
            actual_result = "❌ ไม่พบข้อความแจ้งเตือน"
            status = "FAIL"

        log_result("login01_neg02", actual_result, page=page)
        assert status == "PASS", "❌ ข้อความไม่พบ หรือ สีไม่ถูกต้อง!"
        browser.close()

""" Negative Test Scenario 02 END """


""" Negative Test Scenario 03 START """
# กรณีทดสอบ: ล็อกอินโดยไม่กรอก username และ รหัสบัตรประชาชนผิด ควรแสดงข้อความแจ้งเตือนเป็นสีน้ำเงิน

def test_login01_neg03():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        # ปล่อยช่องรหัสประจำตัวว่าง
        page.locator('input[name="f_uid"]').fill("")
        page.locator('input[name="f_pwd"]').fill("abc25965")
        page.locator('input[name="f_idcard"]').fill("5555")

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            error_element = page.locator(
                "xpath=//font[contains(text(),'กรุณาป้อนรหัสประจำตัวและรหัสผ่านให้ถูกต้อง')]"
            ).first
            assert error_element.is_visible()

            color = error_element.evaluate("el => window.getComputedStyle(el).color")
            print(f"📌 DEBUG: สีของข้อความแจ้งเตือน → {color}")

            if is_blue(color):
                actual_result = "✅ พบข้อความแจ้งเตือน และเป็นสีน้ำเงิน"
                status = "PASS"
            else:
                actual_result = "❌ พบข้อความแจ้งเตือน แต่เป็นสีแดง"
                status = "FAIL"

        except Exception:
            actual_result = "❌ ไม่พบข้อความแจ้งเตือน"
            status = "FAIL"

        log_result("login01_neg03", actual_result, page=page)
        assert status == "PASS", "❌ ข้อความไม่เจอ หรือ สีไม่ถูกต้อง!"
        browser.close()

""" Negative Test Scenario 03 END """
# -------------------------- END NEGATIVE TEST -------------------------- #