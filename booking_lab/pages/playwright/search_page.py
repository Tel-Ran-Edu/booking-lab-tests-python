"""Search page (/) for Playwright: the search form and the result cards."""

from playwright.sync_api import Locator, Page


class SearchPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.city = page.get_by_test_id("search-city")
        self.check_in = page.get_by_test_id("search-check-in")
        self.check_out = page.get_by_test_id("search-check-out")
        self.adults = page.get_by_test_id("search-adults")
        self.submit = page.get_by_test_id("search-submit")
        self.total = page.get_by_test_id("search-total")
        self.loading = page.get_by_test_id("search-loading")
        # every hotel card has data-testid="hotel-card-<id>"; its parts add a suffix
        self.card_links = page.locator('[data-testid^="hotel-card-"][data-testid$="-link"]')

    def open(self) -> "SearchPage":
        self.page.goto("/")
        return self

    def search(self, city: str, check_in: str, check_out: str, adults: int = 2) -> None:
        """Fill the form, submit it and wait for the new results.

        The page already shows hotels before you search, so waiting for any card is not
        enough: wait for the search request to answer and the loading skeleton to go away.
        """
        self.city.fill(city)
        self.check_in.fill(check_in)
        self.check_out.fill(check_out)
        self.adults.fill(str(adults))
        with self.page.expect_response(lambda r: "/api/v1/hotels?" in r.url and "city=" in r.url):
            self.submit.click()
        self.loading.wait_for(state="hidden")

    def card_name(self, hotel_id: str) -> Locator:
        return self.page.get_by_test_id(f"hotel-card-{hotel_id}-name")

    def first_hotel_id(self) -> str:
        """Id of the first hotel in the results, read from its card's data-testid."""
        self.card_links.first.wait_for()
        testid = self.card_links.first.get_attribute("data-testid") or ""
        return testid.removeprefix("hotel-card-").removesuffix("-link")

    def open_hotel(self, hotel_id: str) -> None:
        self.page.get_by_test_id(f"hotel-card-{hotel_id}-link").click()
