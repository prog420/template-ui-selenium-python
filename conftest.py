import logging
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from utils.page_load_strategy import PageLoadStrategy


pytest_plugins = (
    "utils.fixtures.ui_report",
    "utils.fixtures.logger"
)

logger = logging.getLogger("test")


@pytest.hookimpl
def pytest_exception_interact(node, call, report: pytest.TestReport):
    logger.error(f"Error occured: {report.longreprtext}")


@pytest.fixture(scope="session")
def base_temp_directory(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """
    Get base temporary directory which can be changed via --basetemp="<dir>".

    If test run was launched from Gitlab (check predefined CI_BUILDS_DIR var),
    return shared volume between Selenium service and main container
    """
    # "/tmp/downloads" for Selenium Grid
    if os.getenv("CI_BUILDS_DIR"):
        return Path("/builds")
    else:
        return tmp_path_factory.getbasetemp()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--headless", action="store_true")
    parser.addoption("--browser", default="chrome")
    parser.addoption("--remote", action="store_true")


def pytest_configure(config: pytest.Config) -> None:
    """
    Set up required clients (API / SQL) before the test run
    """
    ...


@pytest.fixture(scope="session")
def config(request: pytest.FixtureRequest, base_temp_directory) -> dict:
    """
    This function reads CLI arguments provided via 'pytest_addoption',
    creates Options with settings for different browsers.

    Additional information on '--no-sandbox' and '--disable-shm-usage'
    arguments:
    https://petertc.medium.com/pro-tips-for-selenium-setup-1855a11f88f8
    https://www.google.com/googlebooks/chrome/med_26.html
    """
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    remote = request.config.getoption("--remote")

    if browser == "chrome":
        options = ChromeOptions()
        # Change default download directory
        prefs = {
            "download.default_directory": str(base_temp_directory),
            "profile.default_content_settings.popus": 0,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        options.add_experimental_option("prefs", prefs)
        # Remove notification "Chrome is being controlled by automated software"
        options.add_experimental_option(
            "useAutomationExtension", False
        )
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        # Set logging settings
        options.set_capability(
            "goog:loggingPrefs", {"browser": "ALL"}
        )
    else:
        raise ValueError(f"Browser {browser} is not supported")

    # Arguments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument("--window-size=1920,1080")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--lang=ru_RU")

    # Capabilities
    options.set_capability(
        "pageLoadStrategy", PageLoadStrategy.NORMAL.value
    )
    # For web app which won't open without insecure certs
    options.set_capability("acceptInsecureCerts", True)
    # Selenium Grid capabilities
    if remote:
        options.set_capability("se:noVncPort", 7900)
        options.set_capability("se:vncEnabled", True)

    return {
        "headless": headless,
        "browser": browser,
        "remote": remote,
        "options": options
    }


@pytest.fixture(scope="function")
def driver(config: dict) -> WebDriver:
    """
    Set up driver for browser or tools with remote connection
    (Selenoid / Selenium Grid etc.)
    :param config: dictionary with settings provided via `config` fixture.
    """
    if config["remote"]:
        driver = webdriver.Remote(
            command_executor="http://chrome:4444/wd/hub",
            options=config["options"]
        )
    else:
        if config["browser"] == "chrome":
            driver = webdriver.Chrome(
                options=config["options"]
            )
        else:
            raise ValueError(f"Browser {config["browser"]} is not supported")
    yield driver
    driver.quit()
