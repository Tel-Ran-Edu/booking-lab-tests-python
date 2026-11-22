"""Registration and sign-in through the API (requirements section 3.1)."""

import allure

from booking_lab.data import unique_email


@allure.feature("Account")
def test_register_then_sign_in(api, settings):
    email, password = unique_email(), "Secret1!"

    registered = api.register(email=email, password=password, first_name="Anna",
                              last_name="Levi", cohort_code=settings.cohort)
    assert registered.status_code == 201, registered.text
    assert registered.json()["email"] == email

    signed_in = api.login(email, password)
    assert signed_in.status_code == 200, signed_in.text
    assert signed_in.json()["access_token"]

    api.authorize(signed_in.json()["access_token"])
    me = api.me()
    assert me.status_code == 200
    assert (me.json()["first_name"], me.json()["cohort_code"]) == ("Anna", settings.cohort)

    api.reset_my_data()  # clean up what this user created
