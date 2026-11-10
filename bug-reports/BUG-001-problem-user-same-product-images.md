# BUG-001: problem_user sees the same image on every product

> **Status: DRAFT.** Reproduce this yourself and attach a screenshot before submitting. Linked test: `test_problem_user_products_have_distinct_images`.

| Field | Value |
|---|---|
| Severity | Medium |
| Priority | Low (demo account) |
| Environment | https://www.saucedemo.com, Chromium (Playwright) |
| Test data | user `problem_user` / `secret_sauce` |

## Steps to reproduce
1. Open https://www.saucedemo.com
2. Log in as `problem_user`
3. Look at the product images on the Products page

## Expected result
Each product shows its own image.

## Actual result
All products show the same image.

## Evidence
_Attach screenshot here._
