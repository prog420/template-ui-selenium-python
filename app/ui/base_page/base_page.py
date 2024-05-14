import logging
from abc import abstractmethod
from typing import Tuple, List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from app.ui.base_page.base_page_locators import BasePageLocators
from app.ui.links import Links


logger = logging.getLogger("test")


class BasePage:
    PAGE_URL = Links.BASE_PAGE
    locators = BasePageLocators()

    def __init__(self, driver: WebDriver):
        self.logger = logger
        self.driver = driver
        self.action_chains = ActionChains(self.driver)

    def open(self):
        self.driver.get(self.PAGE_URL)

    def is_opened(self):
        raise NotImplementedError

    def wait(self, timeout=20, poll_frequency=0.5) -> WebDriverWait:
        """
        Base setup for Explicit Waits
        :param timeout: max time (in seconds to wait for condition
        :param poll_frequency: pause between polls
        :return: WebDriverWait
        """
        if timeout is None:
            timeout = 20
        return WebDriverWait(
            driver=self.driver, timeout=timeout, poll_frequency=poll_frequency
        )

    def find_element(
            self, locator: Tuple[str, str], timeout=None
    ) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_element_with_text(
            self, locator: Tuple[str, str], text: str, timeout=None
    ) -> WebElement:
        return self.wait(timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def find_visible_element(
        self, locator: Tuple[str, str], timeout=None
    ) -> WebElement:
        return self.wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_clickable_element(
        self, locator: Tuple[str, str], timeout=None
    ) -> WebElement:
        return self.wait(timeout).until(EC.element_to_be_clickable(locator))

    def find_visible_elements(
            self, locator: Tuple[str, str], timeout=None
    ) -> List[WebElement]:
        return self.wait(timeout).until(
            EC.visibility_of_any_elements_located(locator)
        )

    def is_element_present(
            self, locator: Tuple[str, str], timeout=None
    ) -> bool:
        try:
            self.find_element(locator, timeout)
        except TimeoutException:
            return False
        return True

    def is_not_element_present(
            self, locator: Tuple[str, str], timeout=10
    ) -> bool:
        """
        Check if element is not present on the page for the certain amount
        of time.
        """
        try:
            self.find_element(locator, timeout)
        except TimeoutException:
            return True
        return False

    def is_visible_element_present(
            self, locator: Tuple[str, str], timeout=None
    ):
        try:
            self.find_visible_element(locator, timeout)
        except TimeoutException:
            return False
        return True

    def is_not_visible_element_present(
            self, locator: Tuple[str, str], timeout=None
    ):
        try:
            self.wait(timeout).until_not(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            return False
        return True

    def is_element_with_text_present(
            self, locator: Tuple[str, str], text: str, timeout=None
    ) -> bool:
        try:
            self.find_element_with_text(locator, text, timeout)
        except TimeoutException:
            return False
        return True

    def is_disappeared(self, locator, timeout=10):
        try:
            self.wait(timeout).until_not(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return False
        return True

