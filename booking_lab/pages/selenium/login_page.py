"""Sign-in page (/login) for Selenium WebDriver.

Every element on the site has a stable `data-testid`; locate by it, not by text or CSS classes.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def testid(value: str) -> tuple[str, str]:
    return By.CSS_SELECTOR, f'[data-testid="{value}"]'


class LoginPage:
    COHORT = testid("login-cohort-code")
    EMAIL = testid("login-email")
    PASSWORD = testid("login-password")
    SUBMIT = testid("login-submit")
    NAV_USER = testid("app-nav-user")  # in the header once you are signed in

    def __init__(self, driver: WebDriver, web_url: str) -> None:
        self.driver = driver
        self.web_url = web_url
        self.wait = WebDriverWait(driver, 15)

    def open(self) -> "LoginPage":
        self.driver.get(f"{self.web_url}/login")
        self.wait.until(ec.visibility_of_element_located(self.EMAIL))
        return self

    def _type(self, locator: tuple[str, str], text: str) -> None:
        field = self.driver.find_element(*locator)
        field.clear()
        field.send_keys(text)

    def sign_in(self, cohort: str, email: str, password: str) -> None:
        self._type(self.COHORT, cohort)
        self._type(self.EMAIL, email)
        self._type(self.PASSWORD, password)
        self.driver.find_element(*self.SUBMIT).click()

    def signed_in_user(self) -> str:
        """Header text, for example "Anna · DEMO"; waits until it appears."""
        return self.wait.until(ec.visibility_of_element_located(self.NAV_USER)).text
