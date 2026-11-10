# SauceDemo Web UI Test Automation (Python + Playwright)

![UI tests](https://github.com/srivarshinichary-cpu/saucedemo-ui-tests-python/actions/workflows/ui-tests.yml/badge.svg)

UI test automation framework for the [SauceDemo](https://www.saucedemo.com) practice e-commerce site, built with **Python, Playwright, pytest and GitHub Actions** using the Page Object Model. The repository also includes API testing assets (Postman collection, test documentation and a JMeter load test) for the [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) practice API.

## What it covers

| Area | Details |
|---|---|
| Login | Valid login, bad credentials, empty fields, locked-out user, direct URL access without login, logout |
| Products | Item count, sort by name and price (A-Z, Z-A, low-high, high-low), name/price/image present |
| Cart | Add, add multiple, remove (from inventory and cart pages), continue shopping |
| Checkout | End-to-end order, form validation (first name, last name, postal code), total = subtotal + tax, cancel |
| Known issues | Intentionally broken demo users (`problem_user`, `performance_glitch_user`) documented with `xfail` tests and bug reports |
| Performance | Login response-time check (under 2 s) in the UI suite |
| API testing (Restful-Booker) | Postman collection with assertions, 33 test cases with traceability matrix, 8 API bug reports, regression checklist |
| Load testing (Restful-Booker) | JMeter load test plan and a Locust script in `performance/` |
| CI | GitHub Actions: smoke job first, then full regression; HTML report, screenshots and traces uploaded as artifacts |

## Design

- **Page Object Model** (`pages/`): one class per page (`LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`) so locators live in one place.
- **Fixtures** (`tests/conftest.py`): `inventory` logs in and lands on the products page; page objects are injected into tests.
- **Stable locators**: `data-test` attributes instead of CSS classes.
- **Reliable waits**: assertions use Playwright's auto-waiting `expect(...)`, so tests don't depend on timing and stay stable on slower CI machines.
- **Markers**: `smoke`, `regression`, `negative`, `known_issue`.
- **Evidence on failure**: screenshots and Playwright traces (`test-results/`), plus a self-contained HTML report (`reports/report.html`).

## Project structure

```
pages/          base_page, login_page, inventory_page, cart_page, checkout_page
tests/          conftest, test_login, test_inventory, test_cart, test_checkout, test_known_issues
utils/          helpers (price parsing, ids)
docs/           test-plan.md (UI), test-cases.csv, traceability-matrix.md,
                bug-reports.md, regression-checklist.md (Restful-Booker API)
bug-reports/    BUG-001 .. BUG-003 (SauceDemo UI)
postman/        Restful-Booker Postman collection and environment
performance/    restful-booker-load-test.jmx (JMeter), locustfile.py (Locust),
                README.md, performance-report-template.md
.github/workflows/ui-tests.yml
```

## Run the UI tests locally

Prerequisite: Python 3.9+.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                             # everything
pytest -m smoke                    # smoke only
pytest -m negative                 # negative tests only
pytest -m "not known_issue"        # skip the documented-defect tests
pytest --headed --slowmo 300       # watch the browser
```

The HTML report is written to `reports/report.html`.

## Known issues (SauceDemo UI)

The `problem_user` and `performance_glitch_user` accounts are broken on purpose. Tests for them in `tests/test_known_issues.py` assert the correct behaviour and are marked `xfail`. Write-ups with screenshots and measured timings are in [`bug-reports/`](bug-reports/).

BUG-003 (slow login) is environment-dependent: about 5.4 s on a local machine but 0.10 s on GitHub Actions, so its test is non-strict and may show as XPASS in CI.

## Test execution report (local run)

| Metric | Result |
|---|---|
| Total tests | 30 |
| Passed | 27 |
| Expected failures (documented bugs) | 3 |
| Unexpected failures | 0 |
| Execution time | about 1 minute |

Counts in GitHub Actions can differ slightly, because the slow-login test may report XPASS there (see Known issues).

![Test report summary](screenshots/test-report-summary.png)

## API testing assets (Restful-Booker practice API)

These files test the public [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) API, not SauceDemo.

### Test documentation (`docs/`)

| File | Contents |
|---|---|
| [`test-cases.csv`](docs/test-cases.csv) | 33 test cases with steps, expected results, priority and status |
| [`traceability-matrix.md`](docs/traceability-matrix.md) | Requirements REQ-01 to REQ-10 mapped to test cases |
| [`bug-reports.md`](docs/bug-reports.md) | 8 API defect reports with steps to reproduce, expected vs actual result and severity |
| [`regression-checklist.md`](docs/regression-checklist.md) | Smoke, full regression and retest checklist |

### Postman collection (`postman/`)

18 requests in three folders (Health & Auth, Booking CRUD, Negative tests), each with assertions. Requests are chained through environment variables, so run the collection in order.

- **Postman:** import both files from `postman/`, select the *Restful-Booker (public)* environment and use the Collection Runner.
- **Newman:**
  ```bash
  npm install -g newman
  newman run postman/restful-booker.postman_collection.json \
    -e postman/restful-booker.postman_environment.json
  ```

Some negative requests (negative price, reversed dates) check rules the API does not enforce, so they may fail. They document real defects listed in `docs/bug-reports.md`.

### Performance testing (`performance/`)

- **JMeter:** `restful-booker-load-test.jmx` runs list, create and get requests per virtual user.
  ```bash
  jmeter -n -t performance/restful-booker-load-test.jmx \
    -Jusers=50 -Jrampup=30 -Jloops=5 \
    -l performance/results/results.jtl \
    -e -o performance/results/report
  ```
- **Locust:**
  ```bash
  pip install -r requirements-perf.txt
  locust -f performance/locustfile.py --headless -u 10 -r 2 -t 1m --csv=reports/locust
  ```

Record results in [`performance/performance-report-template.md`](performance/performance-report-template.md). Keep the load small; the target is a shared public API.