# BUG-002: problem_user cannot enter a last name at checkout

> **Status: DRAFT.** Reproduce this yourself and attach a screenshot before submitting. Linked test: `test_problem_user_can_type_last_name`.

| Field | Value |
|---|---|
| Severity | High (blocks checkout) |
| Priority | Low (demo account) |
| Environment | https://www.saucedemo.com, Chromium (Playwright) |
| Test data | user `problem_user` / `secret_sauce` |

## Steps to reproduce
1. Log in as `problem_user`
2. Add "Sauce Labs Backpack" to the cart and open the cart
3. Click Checkout
4. Type a value into the Last Name field

## Expected result
The Last Name field shows the typed text.

## Actual result
The typed text does not appear in the Last Name field, so checkout cannot be completed.

## Evidence
_Attach screenshot here._
