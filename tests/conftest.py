import pytest

from config import PASSWORD, STANDARD_USER
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 720}}


@pytest.fixture
def login_page(page) -> LoginPage:
    lp = LoginPage(page)
    lp.open_login()
    return lp


@pytest.fixture
def inventory(page, login_page) -> InventoryPage:
    """Logged in as the standard user and sitting on the inventory page."""
    login_page.login(STANDARD_USER, PASSWORD)
    return InventoryPage(page)


@pytest.fixture
def cart_page(page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page) -> CheckoutPage:
    return CheckoutPage(page)
