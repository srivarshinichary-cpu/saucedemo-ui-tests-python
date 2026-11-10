import time

import pytest
from playwright.sync_api import expect

from config import BASE_URL, LOCKED_USER, PASSWORD, STANDARD_USER


@pytest.mark.smoke
@pytest.mark.regression
def test_valid_login_opens_inventory(page, login_page, inventory_page):
    login_page.login(STANDARD_USER, PASSWORD)
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(inventory_page.title).to_have_text("Products")


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
    expect(login_page.error).to_contain_text(expected_error)


@pytest.mark.negative
@pytest.mark.regression
def test_locked_out_user_cannot_login(login_page):
    login_page.login(LOCKED_USER, PASSWORD)
    expect(login_page.error).to_contain_text("locked out")


@pytest.mark.negative
@pytest.mark.regression
def test_inventory_requires_login(page, login_page):
    login_page.open("/inventory.html")
    expect(login_page.error).to_contain_text("logged in")
    expect(page).to_have_url(f"{BASE_URL}/")


@pytest.mark.regression
def test_logout_returns_to_login(page, inventory, login_page):
    inventory.logout()
    expect(page).to_have_url(f"{BASE_URL}/")
    expect(login_page.login_button).to_be_visible()


@pytest.mark.regression
def test_standard_user_login_under_two_seconds(page, login_page):
    start = time.perf_counter()
    login_page.login(STANDARD_USER, PASSWORD)
    page.wait_for_url(f"{BASE_URL}/inventory.html")
    elapsed = time.perf_counter() - start
    print(f"standard_user login took {elapsed:.2f}s")
    assert elapsed < 2.0
