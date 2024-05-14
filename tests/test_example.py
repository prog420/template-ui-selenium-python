from tests.base_case import BaseCase
from app.ui.main_page.main_page import MainPage


class TestExample(BaseCase):
    def test_example(self):
        main_page = MainPage(self.driver)
        main_page.open()
        assert main_page.is_opened()
