"""
SauceDemo ships intentionally broken demo users. These tests describe the
CORRECT behaviour, so they are expected to fail (xfail) against the demo site.
If one of them starts passing, the site changed - review the matching bug report.
See bug-reports/ for the write-ups.
"""
import time

import pytest
from playwright.sync_api import expect

from config import BASE_URL, PASSWORD, PERFORMANCE_USER, PROBLEM_USER
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.known_issue


@pytest.mark.xfail(reason="BUG-001: problem_user sees the same image on every product", strict=False)
def test_problem_user_products_have_distinct_images(page):
    login = LoginPage(page)
    login.open_login()
    login.login(PROBLEM_USER, PASSWORD)
    inventory = InventoryPage(page)
    expect(inventory.images).to_have_count(6)  # wait for the page; never compare an empty list
    sources = [img.get_attribute("src") for img in inventory.images.all()]
    assert len(sources) == 6
    assert len(set(sources)) == len(sources)


@pytest.mark.xfail(
    reason="BUG-002: problem_user - text typed into Last Name appears in the First Name field",
    strict=False,
)
def test_problem_user_can_type_last_name(page):
    login = LoginPage(page)
    login.open_login()
    login.login(PROBLEM_USER, PASSWORD)
    inventory = InventoryPage(page)
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.open_cart()
    page.locator('[data-test="checkout"]').click()
    checkout = CheckoutPage(page)
    checkout.last_name.fill("Kumar")
    assert checkout.last_name.input_value() == "Kumar"
    assert checkout.first_name.input_value() == ""


@pytest.mark.xfail(
    reason="BUG-003: performance_glitch_user login is slow (environment-dependent, see bug report)",
    strict=False,
)
def test_performance_user_login_under_two_seconds(page):
    login = LoginPage(page)
    login.open_login()
    start = time.perf_counter()
    login.login(PERFORMANCE_USER, PASSWORD)
    page.wait_for_url(f"{BASE_URL}/inventory.html")
    elapsed = time.perf_counter() - start
    print(f"performance_glitch_user login took {elapsed:.2f}s")
    assert elapsed < 2.0
