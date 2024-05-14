from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver


class BaseCase:
    driver: WebDriver
    download_directory: Path

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, base_temp_directory):
        self.driver = driver
        self.download_directory = base_temp_directory
