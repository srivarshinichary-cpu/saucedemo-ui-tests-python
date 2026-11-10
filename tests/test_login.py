import time

import pytest

from config import BASE_URL, LOCKED_USER, PASSWORD, STANDARD_USER
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.regression
def test_valid_login_opens_inventory(page, login_page):
    login_page.login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(page)
    assert page.url == f"{BASE_URL}/inventory.html"
    assert inventory.title.inner_text() == "Products"


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("wrong_user", PASSWORD, "Username and password do not match"),
        (STANDARD_USER, "wrong_password", "Username and password do not match"),
        ("", PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["bad-user", "bad-password", "no-username", "no-password", "empty-form"],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    login_page.login(username, password)
    assert expected_error in login_page.error_text()


@pytest.mark.negative
@pytest.mark.regression
def test_locked_out_user_cannot_login(login_page):
    login_page.login(LOCKED_USER, PASSWORD)
    assert "locked out" in login_page.error_text()


@pytest.mark.negative
@pytest.mark.regression
def test_inventory_requires_login(page, login_page):
    login_page.open("/inventory.html")
    assert "logged in" in login_page.error_text()
    assert page.url.rstrip("/") == BASE_URL


@pytest.mark.regression
def test_logout_returns_to_login(page, inventory, login_page):
    inventory.logout()
    assert page.url.rstrip("/") == BASE_URL
    assert login_page.login_button.is_visible()


@pytest.mark.regression
def test_standard_user_login_under_two_seconds(page, login_page):
    start = time.perf_counter()
    login_page.login(STANDARD_USER, PASSWORD)
    page.wait_for_url(f"{BASE_URL}/inventory.html")
    elapsed = time.perf_counter() - start
    print(f"standard_user login took {elapsed:.2f}s")
    assert elapsed < 2.0