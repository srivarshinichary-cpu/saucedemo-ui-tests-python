import pytest

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
@pytest.mark.regression
def test_add_item_updates_cart_badge(inventory):
    assert inventory.cart_count() == 0
    inventory.add_to_cart(BACKPACK)
    assert inventory.cart_count() == 1


@pytest.mark.regression
def test_add_multiple_items(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    assert inventory.cart_count() == 2
    inventory.open_cart()
    assert sorted(cart_page.item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.regression
def test_remove_item_from_inventory_page(inventory):
    inventory.add_to_cart(BACKPACK)
    inventory.remove_from_cart(BACKPACK)
    assert inventory.cart_count() == 0


@pytest.mark.regression
def test_remove_item_from_cart_page(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.open_cart()
    cart_page.remove(BACKPACK)
    assert cart_page.item_names() == [BIKE_LIGHT]


@pytest.mark.regression
def test_continue_shopping_returns_to_inventory(page, inventory, cart_page):
    inventory.open_cart()
    cart_page.continue_shopping()
    assert page.url.endswith("/inventory.html")
