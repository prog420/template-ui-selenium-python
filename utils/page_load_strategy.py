from enum import Enum


class PageLoadStrategy(Enum):
    """
    More info about page load strategies:
    https://www.lambdatest.com/blog/selenium-page-load-strategy/
    https://www.selenium.dev/documentation/webdriver/drivers/options/
    """
    NONE = "none"
    NORMAL = "normal"
    EAGER = "eager"
