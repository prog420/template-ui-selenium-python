from selenium.webdriver.common.by import By

from app.ui.base_page.base_page_locators import BasePageLocators


class MainPageLocators(BasePageLocators):
    WEB_INPUT_BTN = (By.XPATH, '//a[@href="/inputs"]')
