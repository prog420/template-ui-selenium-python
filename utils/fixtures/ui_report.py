import os
from uuid import uuid4

import allure
import pytest


@pytest.fixture(scope="function", autouse=True)
def ui_report(driver, request: pytest.FixtureRequest, base_temp_directory):
    """
    Supported driver log types:
        - "logcat": Logs for Android applications on real device and
        emulators via ADB,
        - "bugreport": 'adb bugreport' output for advanced issues diagnostic,
        - "server": Appium server logs
    """
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        # Screenshot
        screenshot_name = f"{request.node.name}_{uuid4()}_screenshot.png"
        screenshot_path = os.path.join(base_temp_directory, screenshot_name)
        driver.get_screenshot_as_file(screenshot_path)
        # Driver Logs
        log_name = f"{request.node.name}_{uuid4()}_driver.log"
        log_path = os.path.join(base_temp_directory, log_name)
        with open(log_path, "w", encoding="utf-8") as f:
            for i in driver.get_log("browser"):
                f.write(f"{i['timestamp']} - {i['level']}\n{i['message']}")
        # Allure
        allure.attach.file(log_path, log_name, allure.attachment_type.TEXT)
        allure.attach.file(
            screenshot_path, screenshot_name, allure.attachment_type.PNG
        )
