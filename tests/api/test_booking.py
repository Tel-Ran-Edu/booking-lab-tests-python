"""Book → pay → cancel through the API (requirements section 3.3)."""

import allure

from booking_lab.data import GOOD_CARD, stay


@allure.feature("Booking")
def test_book_pay_and_cancel(user):
    api = user.api
    dates = stay(days_ahead=45, nights=2)

    with allure.step("Find a room type with a free room for two adults"):
        hotels = api.search_hotels(city="Tel Aviv", adults=2, **dates).json()["items"]
        assert hotels, "no hotel has free rooms on these dates"
        rooms = api.availability(hotels[0]["id"], adults=2, **dates).json()["room_types"]
        room = next(r for r in rooms if r["free_rooms"] > 0 and r["fits_guests"])

    with allure.step("Book it"):
        created = api.create_booking(
            room_type_id=room["id"], **dates,
            adults=[{"first_name": "Anna", "last_name": "Levi"},
                    {"first_name": "Dan", "last_name": "Levi"}],
            phone="+972501234567")
        assert created.status_code == 201, created.text
        booking = created.json()
        assert booking["status"] == "pending_payment"

    with allure.step("Pay with the test card"):
        paid = api.pay(booking["id"], **GOOD_CARD)
        assert paid.status_code == 200, paid.text
        assert api.get_booking(booking["id"]).json()["status"] == "confirmed"

    with allure.step("Cancel it"):
        cancelled = api.cancel(booking["id"])
        assert cancelled.status_code == 200, cancelled.text
        assert api.get_booking(booking["id"]).json()["status"] == "cancelled"
