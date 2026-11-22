"""A small client for the BooKing Lab API (Swagger: <API_URL>/docs).

Every method returns the `requests.Response`, so a test decides what to check: the status code,
the body, the headers. Add a method here when your tests need a new endpoint.
"""

from typing import Any

import requests

TIMEOUT = 30  # seconds per request


class BookingLabApi:
    def __init__(self, api_url: str, cohort: str) -> None:
        self.base = f"{api_url}/api/v1"
        self.session = requests.Session()
        # Requests without a token need the cohort code; with a token the cohort comes from it.
        self.session.headers["X-Workspace"] = cohort

    # --- session ---------------------------------------------------------------------------

    def authorize(self, access_token: str) -> None:
        """Send this token with every next request."""
        self.session.headers["Authorization"] = f"Bearer {access_token}"

    def _call(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        return self.session.request(method, f"{self.base}{path}", timeout=TIMEOUT, **kwargs)

    # --- test helpers (SPEC section 7.1) ---------------------------------------------------

    def create_test_user(self, **fields: Any) -> requests.Response:
        """POST /test/users: a verified user with a random autotest+… email and password."""
        return self._call("POST", "/test/users", json=fields)

    def reset_my_data(self) -> requests.Response:
        """POST /test/reset: delete everything the signed-in user created."""
        return self._call("POST", "/test/reset")

    # --- auth ------------------------------------------------------------------------------

    def register(self, **fields: Any) -> requests.Response:
        return self._call("POST", "/auth/register", json=fields)

    def login(self, email: str, password: str) -> requests.Response:
        return self._call("POST", "/auth/login", json={"email": email, "password": password})

    def me(self) -> requests.Response:
        return self._call("GET", "/users/me")

    # --- hotels ----------------------------------------------------------------------------

    def search_hotels(self, **params: Any) -> requests.Response:
        """GET /hotels with query parameters: city, check_in, check_out, adults, …"""
        return self._call("GET", "/hotels", params=params)

    def availability(self, hotel_id: int, **params: Any) -> requests.Response:
        return self._call("GET", f"/hotels/{hotel_id}/availability", params=params)

    # --- bookings --------------------------------------------------------------------------

    def create_booking(self, **fields: Any) -> requests.Response:
        return self._call("POST", "/bookings", json=fields)

    def get_booking(self, booking_id: int) -> requests.Response:
        return self._call("GET", f"/bookings/{booking_id}")

    def pay(self, booking_id: int, **card: Any) -> requests.Response:
        return self._call("POST", f"/bookings/{booking_id}/pay", json=card)

    def cancel(self, booking_id: int) -> requests.Response:
        return self._call("POST", f"/bookings/{booking_id}/cancel")
