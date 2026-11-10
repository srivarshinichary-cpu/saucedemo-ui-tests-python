import pytest

BACKPACK = "Sauce Labs Backpack"


@pytest.fixture
def at_checkout_form(inventory, cart_page):
    """One item in the cart, standing on checkout step one."""
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()
    cart_page.checkout()


@pytest.mark.smoke
@pytest.mark.regression
def test_end_to_end_checkout(page, at_checkout_form, checkout_page):
    checkout_page.fill_info("Ravi", "Kumar", "500001")
    checkout_page.continue_()
    assert page.url.endswith("/checkout-step-two.html")
    checkout_page.finish()
    assert checkout_page.complete_header.inner_text() == "Thank you for your order!"


@pytest.mark.regression
def test_order_total_equals_subtotal_plus_tax(at_checkout_form, checkout_page):
    checkout_page.fill_info("Ravi", "Kumar", "500001")
    checkout_page.continue_()
    assert checkout_page.total() == pytest.approx(
        checkout_page.subtotal() + checkout_page.tax(), abs=0.01
    )


@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Kumar", "500001", "First Name is required"),
        ("Ravi", "", "500001", "Last Name is required"),
        ("Ravi", "Kumar", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_form_validation(at_checkout_form, checkout_page, first, last, postal, expected_error):
    checkout_page.fill_info(first, last, postal)
    checkout_page.continue_()
    assert expected_error in checkout_page.error_text()


@pytest.mark.regression
def test_cancel_returns_to_cart(page, at_checkout_form, checkout_page):
    checkout_page.cancel_button.click()
    assert page.url.endswith("/cart.html")
