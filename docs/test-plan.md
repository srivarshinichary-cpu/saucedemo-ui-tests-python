# Test Plan: SauceDemo Web UI

## 1. Objective
Verify that the main customer flows of the SauceDemo e-commerce demo site work correctly: login, product browsing, cart and checkout.

## 2. Scope
**In scope:** login and logout, product listing and sorting, add/remove cart items, checkout form validation and order completion.
**Out of scope:** payment gateways (none exist), mobile browsers, accessibility audit, load testing of SauceDemo itself.

## 3. Test types
| Type | How it is covered |
|---|---|
| Smoke | `pytest -m smoke`: login, product list, add to cart, end-to-end checkout |
| Functional / regression | `pytest -m regression`: sorting, cart edits, checkout totals, logout |
| Negative | `pytest -m negative`: bad credentials, locked user, empty form fields, direct URL access without login |
| Known issues | `pytest -m known_issue`: intentional demo defects, expected to fail (xfail) |
| Performance | Locust script in `performance/` against the Restful-Booker API |

## 4. Test environment
- Application: https://www.saucedemo.com (public demo site)
- Browser: Chromium via Playwright, viewport 1280x720
- Tools: Python 3.11, pytest, pytest-playwright, pytest-html, GitHub Actions

## 5. Test data
Public demo accounts: `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user` (password `secret_sauce`). Each test starts from a fresh browser context, so tests are independent and can run in any order.

## 6. Entry and exit criteria
- **Entry:** the site is reachable and the demo accounts log in.
- **Exit:** all smoke and regression tests pass; known-issue tests are either failing as documented or have a bug report; no unreviewed failures.

## 7. Risks
- SauceDemo is a third-party site; it can change locators or be briefly unavailable (mitigation: `data-test` locators, re-run before raising a defect).
- Intentionally broken users can make results look like regressions (mitigation: isolated in the `known_issue` marker).

## 8. Deliverables
HTML report per run, failure screenshots and traces, defect reports in `bug-reports/`, CI results in GitHub Actions.
