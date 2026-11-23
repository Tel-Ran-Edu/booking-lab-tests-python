# BooKing Lab — requirements

> For students. These are sections 3–5 of the BooKing Lab specification: what the system must
> do, the field validation rules and the REST API. Requirement IDs (`REQ-…`) are the same as in
> the specification: put them in your test cases and bug reports. Swagger with every request and
> response: `<API>/docs`.
>
> This file is generated; do not edit it by hand.

## 3. Functional requirements

### 3.1 Registration, sign-in, session

- **REQ-AUTH-001** Registration with email, password, first name, last name and cohort code (workspace code). Wrong cohort code → error "Unknown group code".
- **REQ-AUTH-002** After registration a 6-digit confirmation code arrives in the fake mailbox, valid for 10 minutes. Unconfirmed users cannot book (403).
- **REQ-AUTH-003** Registering again with the same email in the same workspace → 409, "A user with this email already exists". Emails are compared case-insensitively, with surrounding spaces trimmed.
- **REQ-AUTH-004** Sign-in with email and password returns an access token (JWT, 15 minutes) and a refresh token (7 days).
- **REQ-AUTH-005** A wrong password and a non-existent email return the **same** 401 response, "Invalid email or password".
- **REQ-AUTH-006** After 5 failed attempts in a row the account is locked for 5 minutes (423 with a `Retry-After` header).
- **REQ-AUTH-007** Sign-out invalidates the refresh token; reusing it → 401.
- **REQ-AUTH-008** Password reset via a code in the fake mailbox. A reset request for a non-existent email returns the same 200 as for an existing one.
- **REQ-AUTH-009** Changing the password from the profile requires the current password; the new one must differ from the old one.
- **REQ-AUTH-010** In the UI an expired access token is refreshed silently; an expired refresh token → sign-in page with the message "Session expired".

### 3.2 Search and catalog

- **REQ-SRCH-001** Search by city, check-in date, check-out date and number of guests (adults + children). City search is case-insensitive and matches by prefix ("Tel" → "Tel Aviv").
- **REQ-SRCH-002** Results show only hotels with free rooms for ALL nights of the range and capacity of at least the number of guests.
- **REQ-SRCH-003** Filters: price per night (from–to), stars (1–5, multi-select), amenities (Wi-Fi, parking, pool, breakfast, pets — AND condition), review rating from N.
- **REQ-SRCH-004** Sorting: price ↑↓, rating ↓, stars ↓, name A–Z. Ties are broken by ascending id (deterministic order).
- **REQ-SRCH-005** Pagination: 10 per page by default, `page_size` 1–50. The response contains `total`, `page`, `pages`.
- **REQ-SRCH-006** Empty result → message "Nothing found. Change the dates or filters" and a "Reset filters" button.
- **REQ-SRCH-007** Hotel page: photos, description, address, amenities, room types with the price for the selected dates, paginated reviews, average rating (rounded to 0.1).
- **REQ-SRCH-008** Favorites: add / remove a hotel, list of favorites. Adding again is idempotent (200, no duplicates).

### 3.3 Booking

- **REQ-BOOK-001** A booking = room type + dates + guests (first and last name of each adult; age of each child) + contact phone + special requests (optional) + promo code (optional).
- **REQ-BOOK-002** Check-in is not earlier than today (in the hotel's time zone) and not later than 365 days ahead. Check-out is strictly after check-in. Length of stay 1–30 nights.
- **REQ-BOOK-003** Guests: adults 1–room capacity, children 0–4; the total does not exceed capacity. A child is aged 0–17.
- **REQ-BOOK-004** It is impossible to book more rooms than are free on any of the nights → 409 "No rooms available for the selected dates". Two simultaneous requests for the last room → exactly one succeeds.
- **REQ-BOOK-005** Price: sum of nightly rates (prices may differ by day; Friday and Saturday +20%) − promo discount + 17% tax. Rounded to 0.01 (half up) on the total only. All prices are in euros (EUR), in every hotel.
- **REQ-BOOK-006** Promo codes: percentage (1–50%) or fixed amount; validity period; minimum order total; usage limit; one promo code per booking. Code is case-insensitive. The total can never go below 0.
- **REQ-BOOK-007** Statuses: `pending_payment` → `confirmed` → `checked_in` → `completed`; `pending_payment` and `confirmed` can go to `cancelled`; a manager can move `confirmed` → `rejected`. An invalid transition → 409.
- **REQ-BOOK-008** A booking in `pending_payment` is cancelled automatically after 15 minutes without payment, and the room is released.
- **REQ-BOOK-009** Payment stub with test card numbers: `4242 4242 4242 4242` — success; `4000 0000 0000 0002` — declined (402); `4000 0000 0000 9995` — insufficient funds (402); an invalid Luhn checksum → 422. Real cards are neither accepted nor stored.
- **REQ-BOOK-010** Cancellation by the guest: free 7+ days before check-in; 2–6 days — 50% penalty; less than 2 days — 100%. The refund amount is shown before confirmation.
- **REQ-BOOK-011** A booking can be changed (dates, guests, requests) only in `pending_payment` and `confirmed`, no later than 24 hours before check-in; the price is recalculated.
- **REQ-BOOK-012** Every booking has a human-readable number like `BL-2026-000123`; "My bookings" list with a status filter and sorting by check-in date.
- **REQ-BOOK-013** After confirmation and after cancellation an email with the booking number and amount arrives in the fake mailbox.

### 3.4 Reviews

- **REQ-REV-001** A review can be left only for a booking in `completed` status, one per booking, within 30 days after check-out.
- **REQ-REV-002** Rating 1–5 (integer), text 20–1000 characters. Editing allowed for 24 hours after publishing. The manager can reply once.
- **REQ-REV-003** HTML in review text is escaped and shown as text (XSS protection).

### 3.5 Hotel manager area

- **REQ-MGR-001** CRUD for hotels, room types (name, capacity, number of rooms, base price) and rates for specific dates.
- **REQ-MGR-002** A hotel or room type with future active bookings cannot be deleted → 409. The number of rooms cannot be reduced below the number already booked.
- **REQ-MGR-003** List of bookings across own hotels with filters; check-in (on the arrival day) and check-out.
- **REQ-MGR-004** Report: occupancy by day (%) and revenue for a period; CSV export.

### 3.7 Localization

- **REQ-I18N-001** UI and API messages are in English only.

## 4. Field validation rules

Boundaries are exact so students can build equivalence classes and boundary values. Text fields are trimmed before validation. All errors of one request are returned at once, as a list per field.

| Field | Required | Rule | Error message |
| --- | --- | --- | --- |
| Email | yes | RFC 5322 (simplified), 6–100 characters, no inner spaces | "Enter a valid email" |
| Password | yes | 8–20 characters; at least 1 uppercase, 1 lowercase Latin letter, 1 digit, 1 special character from `!@#$%^&*`; no spaces, no Cyrillic | the specific rule that failed |
| Confirm password | yes (UI) | matches the password | "Passwords do not match" |
| First name, last name | yes | 2–50 characters; letters of any alphabet, space, hyphen, apostrophe; no digits | "Letters, space, hyphen and apostrophe only" |
| Phone | yes (booking) | E.164: `+` and 8–15 digits; spaces and hyphens allowed in the UI and stripped | "Phone in international format: +972…" |
| Date of birth (profile) | no | ISO `YYYY-MM-DD`; age 18–120 | "You must be at least 18" |
| Cohort code | yes | 4–12 characters, `A–Z`, `0–9`, hyphen; case-insensitive | "Unknown group code" |
| Booking dates | yes | REQ-BOOK-002 | "Check-out must be after check-in" etc. |
| Adults / children | yes / no | integers; REQ-BOOK-003 | "Room capacity exceeded" |
| Special requests | no | 0–500 characters, counter in the UI | "Maximum 500 characters" |
| Promo code | no | 4–16 characters, `A–Z0–9` | "Promo code not found / expired / not applicable" (separate messages) |
| Card (stub) | yes | 16 digits + Luhn; expiry `MM/YY` not in the past; CVC 3 digits; cardholder name in Latin letters | per field |
| Hotel name | yes | 3–100 characters, unique within the city in a workspace | "A hotel with this name already exists in this city" |
| Stars | yes | integer 1–5 | — |
| Price per night | yes | 1.00–10,000.00, at most 2 decimal places | — |
| Room capacity | yes | integer 1–8 | — |
| Hotel photo / avatar | no | JPG/PNG/WebP, up to 2 MB, up to 10 photos per hotel | "File larger than 2 MB", "Unsupported format" |

In the UI a field error appears under the field with `data-testid="<field>-error"`; the submit button is always enabled so server-side validation can be tested. Success and server errors are shown as a toast with `data-testid="toast"` and a `data-type="success|error"` attribute, visible for 5 seconds.

## 5. REST API

Base path `/api/v1`, JSON, authorization `Authorization: Bearer <access_token>`. The workspace is taken from the token; for anonymous requests — from the `X-Workspace: <cohort code>` header. Swagger UI at `/docs`, OpenAPI 3.1 schema at `/openapi.json` (imports into Postman in one click). Swagger includes request examples and every response variant, errors included.

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| POST | `/auth/register` | registration | 201 |
| POST | `/auth/verify-email` | confirm with code | 200 |
| POST | `/auth/login` | sign-in, issue tokens | 200 |
| POST | `/auth/refresh` | new access token | 200 |
| POST | `/auth/logout` | revoke refresh token | 204 |
| POST | `/auth/password/forgot`, `/auth/password/reset` | password reset | 200 |
| GET / PATCH | `/users/me` | profile | 200 |
| PUT | `/users/me/password` | change password | 204 |
| POST / DELETE | `/users/me/avatar` | upload and delete avatar (multipart) | 201 / 204 |
| GET | `/hotels` | search: `city`, `check_in`, `check_out`, `adults`, `children`, `price_min`, `price_max`, `stars`, `amenities`, `sort`, `page`, `page_size` | 200 |
| GET | `/hotels/{id}` | hotel page | 200 |
| GET | `/hotels/{id}/availability` | free rooms and prices for dates | 200 |
| POST / PUT / PATCH / DELETE | `/hotels`, `/hotels/{id}` | hotel management (manager) | 201 / 200 / 200 / 204 |
| CRUD | `/hotels/{id}/room-types`, `/room-types/{id}/rates` | rooms and rates (manager) | — |
| POST | `/bookings/quote` | price calculation without creating a booking | 200 |
| POST | `/bookings` | create a booking | 201 + `Location` |
| GET | `/bookings`, `/bookings/{id}` | my bookings / one booking | 200 |
| PATCH | `/bookings/{id}` | change a booking | 200 |
| POST | `/bookings/{id}/pay`, `/cancel`, `/confirm`, `/reject`, `/check-in`, `/check-out` | status transitions | 200 |
| GET / POST / PATCH / DELETE | `/hotels/{id}/reviews`, `/reviews/{id}` | reviews | 200 / 201 / 200 / 204 |
| PUT / DELETE / GET | `/favorites/{hotel_id}`, `/favorites` | favorites | 200 / 204 / 200 |
| GET | `/promo-codes/{code}` | check a promo code | 200 |
| GET | `/mailbox` | fake mailbox of the current user | 200 |
| GET | `/manager/reports/occupancy`, `/manager/reports/revenue` | reports (JSON or CSV via `Accept`) | 200 |
| POST | `/test/users`, `/test/reset`, `/test/seed` | test data: a verified test user, delete my data, a data set by scenario | 201 / 200 / 201 |
| GET | `/health` | service health (no auth) | 200 |

**Error codes — strictly by meaning:** 400 — malformed JSON or parameter; 401 — missing or expired token; 403 — no permission (role, unverified email); 404 — not found **or someone else's object** (we do not reveal other users' bookings); 405 — method not supported; 409 — state conflict (duplicate, no rooms, invalid transition); 412 — stale version (`If-Match`); 413 — file too large; 415 — wrong `Content-Type`; 422 — field validation rules violated; 423 — account temporarily locked; 429 — rate limit exceeded; 500 / 503 — server error.

**Unified error format:**

```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": [{"field": "password", "code": "too_short", "message": "Minimum 8 characters"}],
  "request_id": "9f1c2e7a-..."
}
```

- Every response carries an `X-Request-Id` header — students attach it to bug reports.
- `POST /bookings` accepts an `Idempotency-Key` header: a repeat with the same key returns the same booking instead of creating a new one.
- Updates of bookings and hotels support `ETag` / `If-Match`: a stale version → 412.
- Rate limit: 300 requests per minute per user, 10 sign-in attempts per minute per IP; headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.
- Dates in ISO 8601; money as a string with 2 decimals (`"1234.50"`) plus a currency code, to avoid float rounding errors.

## Templates

### Test case

| Field | Value |
| --- | --- |
| ID | TC-… |
| Title | what is checked, in one line |
| Requirement | REQ-… |
| Preconditions | user, cohort, data that must exist (for example from `POST /test/seed`) |
| Test data | exact values, including boundary values |
| Steps | 1. … 2. … 3. … |
| Expected result | from the requirement: status code, message, what the page shows |
| Priority | High / Medium / Low |
| Type | positive / negative / boundary |

### Bug report

| Field | Value |
| --- | --- |
| ID | BR-… |
| Title | what is wrong, where — short and specific |
| Environment | local or cloud copy; app version (`GET /health` or page footer); browser, OS |
| Cohort | your cohort code |
| Requirement | REQ-… that is violated |
| Preconditions | user, data, settings |
| Steps to reproduce | 1. … 2. … 3. (exact values) |
| Expected result | what the requirement says should happen |
| Actual result | what happened: status code, response body, message |
| `X-Request-Id` | from the response headers, or the id shown in the error message |
| Severity | S1 critical / S2 major / S3 minor / S4 trivial |
| Priority | High / Medium / Low |
| Attachments | screenshot, video, HAR file, request and response |
