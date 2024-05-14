from app.ui.base_page.base_page import BasePage
from app.ui.main_page.main_page_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    # Elements
    @property
    def web_inputs_page_btn(self):
        return self.find_clickable_element(self.locators.WEB_INPUT_BTN)

    # Actions
    def go_to_web_inputs_page(self):
        self.web_inputs_page_btn.click()

    # Checks
    def is_opened(self):
        return self.is_element_present(self.locators.WEB_INPUT_BTN)
