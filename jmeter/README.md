# JMeter plan

`booking-lab.jmx` is a JMeter 5.6 plan for the **local copy** of BooKing Lab (`docker compose up`).
Never run it against the cloud copy: load tests there are forbidden and blocked by rate limits.
The plan checks the target first and stops at once if it is not `localhost`, `127.0.0.1` or
`host.docker.internal`.

## What it does

The thread groups run one after another:

| Thread group | Users × loops (default) | What each user does |
| --- | --- | --- |
| Setup | 1 | checks the target, creates a hotel with a single room for the race |
| Search | 10 × 10 | searches a random city, opens a hotel, looks at its free rooms |
| Booking | 5 × 3 | a new test user books a room, pays, cancels and deletes its data |
| Last room race | 10 × 1 | all users book the hotel's only room for the same dates at the same moment |
| Teardown | 1 | deletes the race hotel |

In the race, each answer is `201` (booked) or `409` (no rooms left). How many `201`s are
right? The requirements (REQ-BOOK-004) say; count them in your results.

## Run it

With JMeter installed (Java 17+), open the plan in the GUI to read and change it:

```bash
jmeter -t jmeter/booking-lab.jmx
```

For a real measurement, run it without the GUI and build the HTML dashboard:

```bash
jmeter -n -t jmeter/booking-lab.jmx -l results.jtl -e -o jmeter-report
```

Without installing JMeter, with Docker (macOS and Windows):

```bash
docker run --rm -v "$PWD/jmeter:/plan" -v "$PWD/out:/out" alpine/jmeter:5.6.3 -n -t /plan/booking-lab.jmx -l /out/results.jtl -e -o /out/report -Jhost=host.docker.internal
```

On Linux, replace `-Jhost=host.docker.internal` with `--network host` before the image name.
Open `out/report/index.html` for the dashboard.

## Settings

Change them with `-Jname=value`:

| Property | Default | Meaning |
| --- | --- | --- |
| `host`, `port`, `protocol` | `localhost`, `8000`, `http` | where the API is |
| `cohort` | `DEMO` | cohort code |
| `rampup` | `5` | seconds to start all users of a thread group |
| `search.users`, `search.loops` | `10`, `10` | the Search thread group |
| `booking.users`, `booking.loops` | `5`, `3` | the Booking thread group |
| `race.users` | `10` | users in the race |

The target from the requirements (REQ-NFR-003): API p95 ≤ 300 ms with 50 concurrent users, on
the local copy without chaos mode. Try `-Jsearch.users=50`.

Every user the plan creates is an `autotest+…` test user; the plan deletes their data, and
the users themselves are removed automatically after 24 hours.
