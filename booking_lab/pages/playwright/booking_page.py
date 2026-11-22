"""Booking form (/book) for Playwright: guests, phone and the price of the stay."""

from playwright.sync_api import Page


class BookingPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.form = page.get_by_test_id("booking-form")
        self.phone = page.get_by_test_id("booking-phone")
        self.special_requests = page.get_by_test_id("booking-special-requests")
        self.subtotal = page.get_by_test_id("booking-quote-subtotal")
        self.tax = page.get_by_test_id("booking-quote-tax")
        self.total = page.get_by_test_id("booking-quote-total")
        self.submit = page.get_by_test_id("booking-submit")

    def adult_name(self, index: int, first: str, last: str) -> None:
        """Adults are numbered from 0."""
        self.page.get_by_test_id(f"booking-adult-{index}-first-name").fill(first)
        self.page.get_by_test_id(f"booking-adult-{index}-last-name").fill(last)
