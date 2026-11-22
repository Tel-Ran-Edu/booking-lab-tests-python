"""Sign-in page (/login) for Playwright. The same page as pages/selenium/login_page.py."""

from playwright.sync_api import Locator, Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cohort = page.get_by_test_id("login-cohort-code")
        self.email = page.get_by_test_id("login-email")
        self.password = page.get_by_test_id("login-password")
        self.submit = page.get_by_test_id("login-submit")
        self.nav_user: Locator = page.get_by_test_id("app-nav-user")

    def open(self) -> "LoginPage":
        self.page.goto("/login")
        return self

    def sign_in(self, cohort: str, email: str, password: str) -> None:
        self.cohort.fill(cohort)
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
