"""Sign-in on the website with Selenium WebDriver."""

import allure

from booking_lab.pages.selenium.login_page import LoginPage


@allure.feature("Account")
def test_sign_in_shows_my_name(driver, settings, user):
    page = LoginPage(driver, settings.web_url).open()

    page.sign_in(settings.cohort, user.email, user.password)

    header = page.signed_in_user()
    assert user.first_name in header
    assert settings.cohort in header
