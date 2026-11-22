"""Hotel search through the API (requirements section 3.2)."""

import allure

from booking_lab.data import stay


@allure.feature("Search")
def test_search_by_city_and_dates(api):
    response = api.search_hotels(city="Haifa", adults=2, **stay(days_ahead=30))

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] > 0
    assert body["items"], "the first page has hotels"
    for hotel in body["items"]:
        assert hotel["city"] == "Haifa"
        # money is a string with 2 decimals, never a float
        assert isinstance(hotel["price_per_night"], str) and "." in hotel["price_per_night"]
