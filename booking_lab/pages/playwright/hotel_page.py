"""Hotel page (/hotels/<id>) for Playwright: hotel details and its room types."""

from playwright.sync_api import Locator, Page


class HotelPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.root = page.get_by_test_id("hotel-page")
        self.name = page.get_by_test_id("hotel-name")
        self.room_types = page.get_by_test_id("hotel-room-types")
        # "<n> rooms left" for each room type that still has free rooms
        self.free_rooms = page.locator('[data-testid^="hotel-room-type-"][data-testid$="-free"]',
                                       has_text="rooms left")

    def first_free_room_type_id(self) -> str:
        self.free_rooms.first.wait_for()
        testid = self.free_rooms.first.get_attribute("data-testid") or ""
        return testid.removeprefix("hotel-room-type-").removesuffix("-free")

    def book_button(self, room_type_id: str) -> Locator:
        return self.page.get_by_test_id(f"hotel-room-type-{room_type_id}-book")
