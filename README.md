# BooKing Lab — Python autotests

A starting project for testing [BooKing Lab](https://booking-lab-2iu.pages.dev), the hotel booking
training app: API tests with `requests`, UI tests with Selenium and Playwright, all run by
`pytest`, with Allure results. It already has five working tests; you add the rest.

## Requirements

`docs/requirements.md` is what BooKing Lab must do: the functional requirements, the
field validation rules and the REST API, with requirement IDs (`REQ-…`) to put in your test
cases and bug reports. It ends with templates for both.

## What you need

- Python 3.12 or newer
- Docker Desktop (for the local copy of BooKing Lab)
- Google Chrome (for the Selenium test)

## Quick start

1. Create your own repository from this template: **Use this template → Create a new
   repository**, then clone it.
2. Start the local copy of BooKing Lab (website, API and database):

   ```bash
   docker compose up -d --wait
   ```

   Website: http://localhost:5173 · API and Swagger: http://localhost:8000/docs

3. Install the test tools in a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

4. Run the tests:

   ```bash
   pytest
   ```

   You should see `5 passed`. Add `HEADED=1` (Selenium) or `--headed` (Playwright) to watch the
   browser: `HEADED=1 pytest --headed`.

Stop the local copy with `docker compose down`. Add `-v` to also delete its data.

## Settings

The tests read three environment variables:

| Variable | Default | Meaning |
| --- | --- | --- |
| `API_URL` | `http://localhost:8000` | The API |
| `WEB_URL` | `http://localhost:5173` | The website |
| `COHORT` | `DEMO` | Your cohort code (`DEMO` is open for self-study) |

To run against the cloud copy with your cohort code:

```bash
API_URL=https://booking-lab-api.onrender.com WEB_URL=https://booking-lab-2iu.pages.dev COHORT=QA80 pytest
```

The cloud copy sleeps after 15 minutes without requests and needs about a minute to wake up.
Never run load tests against it: use the local copy.

## What is inside

```
booking_lab/
  config.py               settings from the environment
  api_client.py           one method per API endpoint; returns the raw response
  data.py                 dates relative to today, unique emails, the test card
  pages/selenium/         page objects for Selenium (sign-in page)
  pages/playwright/       page objects for Playwright (sign-in, search, hotel, booking form)
tests/
  conftest.py             fixtures: settings, api, user, driver, base_url
  api/                    API tests
  ui/                     UI tests
docker-compose.yml        the local copy of BooKing Lab, an exact version
postman/                  the course Postman collection and its environments
jmeter/                   a JMeter load test plan for the local copy
docs/requirements.md      the requirements, a test case and a bug report template
docs/sniffing.md          reading HTTP traffic: DevTools, HTTP Toolkit, a phone, mitmproxy
.github/workflows/        CI: starts BooKing Lab and runs pytest on every push; builds the report
allurerc.mjs              Allure report settings
scripts/report-summary.mjs   pass/fail table for the CI summary
Jenkinsfile               the same pipeline for Jenkins
```

| Test | Tool | Flow |
| --- | --- | --- |
| `tests/api/test_auth.py` | requests | register → sign in → read my profile |
| `tests/api/test_search.py` | requests | search hotels by city and dates |
| `tests/api/test_booking.py` | requests | book a room → pay → cancel |
| `tests/ui/test_sign_in_selenium.py` | Selenium | sign in on the website |
| `tests/ui/test_search_playwright.py` | Playwright | search → hotel page → booking form |

### Fixtures

- `user` creates a new verified user in your cohort through `POST /test/users` (no email step)
  and gives you its email, password and an API client already signed in. After the test it
  calls `POST /test/reset`, which deletes everything that user created. Test users
  (`autotest+…` emails) are also deleted automatically after 24 hours.
- `api` is an API client without a token; `driver` is Chrome for Selenium; `page` is a
  Playwright page (from `pytest-playwright`) that opens paths relative to `WEB_URL`.

### Locators

Every element on the website has a stable `data-testid`, for example `login-email` or
`hotel-card-12-link`. Locate by it: in Selenium `[data-testid="login-email"]`, in Playwright
`page.get_by_test_id("login-email")`. Texts and CSS classes may change; test ids do not.

## Reading the traffic

`docs/sniffing.md` shows how to watch and change the requests between the website (or a phone)
and the API: Chrome DevTools, HTTP Toolkit, a phone over Wi-Fi and mitmproxy. Practise on the
website's **UI lab → Sniffer** page (`/lab/sniffer`).

## Your first task: the cold start

Open `tests/conftest.py` and find the `server_is_awake` fixture. It asks `/health` once, which
works for the local copy but fails when the cloud copy is asleep. Finish it as its docstring
says: ask every 5 seconds for up to 120 seconds, and fail at once with a clear message when
the database is down. Then run the tests against the cloud copy after it has slept.

## Reports

Every run writes Allure results to `allure-results/`. To build the report on your machine
(needs Node.js, no Java):

```bash
npx allure@3.33.0 generate allure-results
```

Then open `allure-report/index.html`: it is one file, so a double-click works, and you can send
it to someone as it is. Settings are in `allurerc.mjs`.

In GitHub Actions every run gets the same report as the `allure-report` artifact (Actions → the
run → Artifacts) and a pass/fail table on the run's summary page.

## Publish your report as a portfolio link

Your CI can publish the latest report as a web page, with the trend of earlier runs, at
`https://<your-user>.github.io/<your-repo>/`. Put that link in your CV or LinkedIn.

1. Open your repository's **Settings → Pages** and set **Source** to **GitHub Actions**.
2. Push to the main branch (or open **Actions → Tests → Run workflow**).
3. When the run is green, the `pages` job shows the link; it is also in Settings → Pages.

Each push to the main branch adds a point to the trend (the last 20 runs are kept), including
red runs: a report that shows how you fixed things is a good portfolio too.

- While Pages is off, the `pages` job is **skipped**, not failed: the run stays green.
- Free GitHub accounts can publish Pages only from public repositories.
- Everyone with the link sees the report: test names, steps and error messages. It holds only
  test data, so keep it that way: no real names, phones, cards or passwords in your tests.

## Postman

`postman/` holds the course collection (reviews, promo codes, favorites, the manager area and
the mailbox) and two environments: `localhost` and the cloud copy (`Render`).

- **In Postman:** Import → choose the three files, pick the environment at the top right, then
  open the collection and press **Run**. Each run creates its own test user and deletes its data
  at the end. Set `cohort` in the environment to your cohort code.
- **With Newman** (Node.js):

  ```bash
  npx newman run postman/booking-lab-course.postman_collection.json -e postman/localhost.postman_environment.json
  ```

- The `postman` job in CI runs the same command. To switch it off, add a repository variable
  `RUN_POSTMAN` with the value `false` (Settings → Secrets and variables → Actions → Variables).
- Cold start: the `Health` request's description has the same task as above, for a Postman
  pre-request script.

## JMeter

`jmeter/booking-lab.jmx` is a load test plan for the local copy: search, booking and a race of
ten users for a hotel's last room. Its README (`jmeter/README.md`) says how to run it with
JMeter or Docker. Never run it against the cloud copy.

## Jenkins

`Jenkinsfile` runs the same steps as the GitHub workflow. In Jenkins, create a
**Pipeline** job with **Pipeline script from SCM**, point it at your repository and keep the
script path `Jenkinsfile`. What the agent needs is listed at the top of the file. The report
is archived with each build as `allure-report/index.html`.

## Troubleshooting

- **429 Too Many Requests on sign-in.** BooKing Lab allows 100 sign-ins per minute from one
  address, like the cloud copy. Wait a minute (the `Retry-After` header says how long), or give
  the local copy a higher limit: `RATE_LIMIT_LOGIN_PER_MINUTE=300 docker compose up -d --wait`.
- **Port 5432, 8000 or 5173 is already in use.** Another program (or another copy of BooKing
  Lab) uses it. Stop it, or change the left side of the port in `docker-compose.yml`.
- **"BooKing Lab is not ready".** The server is not up yet: see the cold start task above.

Use only test data. Do not enter real names, phone numbers or cards.
