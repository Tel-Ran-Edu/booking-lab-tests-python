"""Search → hotel page → booking form on the website with Playwright."""

import re

import allure
from playwright.sync_api import Page, expect

from booking_lab.data import stay
from booking_lab.pages.playwright.booking_page import BookingPage
from booking_lab.pages.playwright.hotel_page import HotelPage
from booking_lab.pages.playwright.login_page import LoginPage
from booking_lab.pages.playwright.search_page import SearchPage

MONEY = re.compile(r"\d+\.\d{2}")


@allure.feature("Search")
def test_search_open_hotel_and_see_the_price(page: Page, settings, user):
    login = LoginPage(page).open()
    login.sign_in(settings.cohort, user.email, user.password)
    expect(login.nav_user).to_contain_text(user.first_name)

    search = SearchPage(page).open()
    dates = stay(days_ahead=40, nights=2)
    search.search("Haifa", dates["check_in"], dates["check_out"], adults=2)
    expect(search.total).to_be_visible()

    hotel_id = search.first_hotel_id()
    name = search.card_name(hotel_id).inner_text()
    search.open_hotel(hotel_id)

    hotel = HotelPage(page)
    expect(hotel.name).to_have_text(name)
    room_type_id = hotel.first_free_room_type_id()
    hotel.book_button(room_type_id).click()

    booking = BookingPage(page)
    expect(booking.form).to_be_visible()
    expect(booking.total).to_contain_text(MONEY)
