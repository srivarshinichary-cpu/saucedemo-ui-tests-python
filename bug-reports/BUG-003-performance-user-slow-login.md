# BUG-003: performance_glitch_user login is slow

> **Status: DRAFT.** Measure this yourself and record the actual time before submitting. Linked test: `test_performance_user_login_under_two_seconds`.

| Field | Value |
|---|---|
| Severity | Medium |
| Priority | Low (demo account) |
| Environment | https://www.saucedemo.com, Chromium (Playwright) |
| Test data | user `performance_glitch_user` / `secret_sauce` |

## Steps to reproduce
1. Open https://www.saucedemo.com
2. Log in as `performance_glitch_user`
3. Measure the time until the Products page loads

## Expected result
Login completes in under 2 seconds.

## Actual result
Login takes noticeably longer. Record the measured time here: ___ seconds.

## Evidence
_Attach the Playwright trace or timing output here._
