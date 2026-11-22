"""Shared fixtures: settings, the API client, a fresh test user, and the browsers."""

import os
from collections.abc import Iterator
from dataclasses import dataclass

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from booking_lab.api_client import BookingLabApi
from booking_lab.config import Settings, load_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session", autouse=True)
def server_is_awake(settings: Settings) -> None:
    """Cold start: wait until BooKing Lab is ready before any test runs.

    The cloud copy of BooKing Lab sleeps after 15 minutes without requests and needs about a
    minute to wake up. Right now this fixture asks /health once, which is enough for the local
    copy started with `docker compose up --wait`, but not for the cloud.

    YOUR TASK (REQ-OPS-003 in the requirements):
    - ask GET /health every 5 seconds until it answers 200, for at most 120 seconds;
    - if the server is still not ready after 120 seconds, fail with a clear message;
    - if /health answers 503 with "db": "down", fail at once with a database message:
      waiting will not help, tell your instructor.
    """
    response = requests.get(f"{settings.api_url}/health", timeout=10)
    assert response.status_code == 200, f"BooKing Lab is not ready: {response.status_code}"


@pytest.fixture
def api(settings: Settings) -> BookingLabApi:
    """An API client without a token."""
    return BookingLabApi(settings.api_url, settings.cohort)


@dataclass
class TestUser:
    __test__ = False  # not a test class, even though its name starts with "Test"
    email: str
    password: str
    first_name: str
    api: BookingLabApi  # already signed in as this user


@pytest.fixture
def user(settings: Settings) -> Iterator[TestUser]:
    """A new verified user in your cohort; after the test, everything it created is deleted."""
    client = BookingLabApi(settings.api_url, settings.cohort)
    response = client.create_test_user()
    assert response.status_code == 201, response.text
    body = response.json()
    client.authorize(body["access_token"])
    yield TestUser(body["user"]["email"], body["password"], body["user"]["first_name"], client)
    client.reset_my_data()


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Chrome for Selenium. Headless unless HEADED=1. Selenium downloads the driver itself."""
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADED") != "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    """Playwright opens page.goto("/login") relative to this address."""
    return settings.web_url
