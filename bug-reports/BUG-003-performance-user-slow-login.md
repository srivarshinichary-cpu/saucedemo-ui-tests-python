# BUG-003: performance_glitch_user login is slow (environment-dependent)

**Status:** Reproduced locally, NOT reproduced on GitHub Actions. Verified 2026-11-10 with automated timing (Playwright, Chromium). Linked test: `test_performance_user_login_under_two_seconds`.

| Field | Value |
|---|---|
| Severity | Medium |
| Priority | Low (demo account) |
| Test data | user `performance_glitch_user` / `secret_sauce` |

## Steps to reproduce
1. Open https://www.saucedemo.com
2. Enter `performance_glitch_user` and `secret_sauce`
3. Click **Login** and measure the time until the Products page (`/inventory.html`) loads

## Expected result
Login completes in under 2 seconds, as it does for a normal user.

## Actual result
The result depends on where the test runs.

| Environment | performance_glitch_user | standard_user (baseline) |
|---|---|---|
| Local laptop, Windows, India: run 1 | 5.37 s | 0.29 s |
| Local laptop: run 2 | 5.41 s | |
| Local laptop: run 3 | 5.36 s | |
| Local laptop: one earlier run, older test version | under 2 s (passed, time not printed) | |
| GitHub Actions (Ubuntu runner) | 0.10 s | |

Timing starts at the click on Login and stops when the URL becomes `/inventory.html`.

## Notes
- The delay of about 5.4 seconds appeared in 3 of 4 local runs but did not appear on GitHub Actions. The cause is not known; it could depend on the network location, the site's deployment, or timing.
- Because of this, the linked test is marked `xfail` (non-strict) and may pass in some environments.
- `performance_glitch_user` is a deliberately degraded demo account.

## Evidence
Local runs:
```
performance_glitch_user login took 5.37s
performance_glitch_user login took 5.41s
performance_glitch_user login took 5.36s
standard_user login took 0.29s
```
GitHub Actions run #1:
```
performance_glitch_user login took 0.10s
```
