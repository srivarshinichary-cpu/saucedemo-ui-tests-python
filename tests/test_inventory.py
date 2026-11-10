import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.regression
def test_inventory_lists_six_products(inventory):
    expect(inventory.items).to_have_count(6)


@pytest.mark.regression
@pytest.mark.parametrize(
    "option, reverse",
    [("lohi", False), ("hilo", True)],
    ids=["price-low-to-high", "price-high-to-low"],
)
def test_sort_by_price(inventory, option, reverse):
    inventory.sort_by(option)
    prices = inventory.product_prices()
    assert prices == sorted(prices, reverse=reverse)


@pytest.mark.regression
@pytest.mark.parametrize(
    "option, reverse",
    [("az", False), ("za", True)],
    ids=["name-a-to-z", "name-z-to-a"],
)
def test_sort_by_name(inventory, option, reverse):
    inventory.sort_by(option)
    names = inventory.product_names()
    assert names == sorted(names, reverse=reverse)


@pytest.mark.regression
def test_every_product_has_name_price_and_image(inventory):
    expect(inventory.items).to_have_count(6)  # wait for the page to finish rendering
    count = inventory.items.count()
    assert len(inventory.product_names()) == count
    assert all(price > 0 for price in inventory.product_prices())
    assert inventory.images.count() == count