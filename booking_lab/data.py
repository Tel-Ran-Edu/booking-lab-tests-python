"""Test data helpers: dates relative to today, unique emails, a test card."""

import uuid
from datetime import date, timedelta

# A test card that always pays successfully (see the payment page of the website)
GOOD_CARD = {"card_number": "4242 4242 4242 4242", "expiry": "12/30", "cvc": "123",
             "cardholder": "Anna Levi"}


def day(offset: int) -> str:
    """Today + offset days as YYYY-MM-DD."""
    return (date.today() + timedelta(days=offset)).isoformat()


def stay(days_ahead: int = 30, nights: int = 2) -> dict[str, str]:
    """check_in / check_out for a stay that starts days_ahead days from today."""
    return {"check_in": day(days_ahead), "check_out": day(days_ahead + nights)}


def unique_email() -> str:
    """autotest+… emails are deleted automatically after 24 hours."""
    return f"autotest+{uuid.uuid4().hex[:12]}@bookinglab.test"
