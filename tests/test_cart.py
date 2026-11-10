import re

import pytest
from playwright.sync_api import expect

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
@pytest.mark.regression
def test_add_item_updates_cart_badge(inventory):
    expect(inventory.cart_badge).to_have_count(0)
    inventory.add_to_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")


@pytest.mark.regression
def test_add_multiple_items(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    expect(inventory.cart_badge).to_have_text("2")
    inventory.open_cart()
    expect(cart_page.names).to_have_count(2)
    assert sorted(cart_page.item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.regression
def test_remove_item_from_inventory_page(inventory):
    inventory.add_to_cart(BACKPACK)
    inventory.remove_from_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_count(0)


@pytest.mark.regression
def test_remove_item_from_cart_page(inventory, cart_page):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.open_cart()
    cart_page.remove(BACKPACK)
    expect(cart_page.names).to_have_text([BIKE_LIGHT])


@pytest.mark.regression
def test_continue_shopping_returns_to_inventory(page, inventory, cart_page):
    inventory.open_cart()
    cart_page.continue_shopping()
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
