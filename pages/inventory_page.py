from pages.base_page import BasePage
from utils.helpers import money, slug


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.names = page.locator('[data-test="inventory-item-name"]')
        self.prices = page.locator('[data-test="inventory-item-price"]')
        self.images = page.locator(".inventory_item_img img")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def product_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def product_prices(self) -> list[float]:
        return [money(p) for p in self.prices.all_inner_texts()]

    def sort_by(self, option_value: str) -> None:
        """option_value is one of: az, za, lohi, hilo."""
        self.sort_dropdown.select_option(option_value)

    def add_to_cart(self, product_name: str) -> None:
        self.page.locator(f'[data-test="add-to-cart-{slug(product_name)}"]').click()

    def remove_from_cart(self, product_name: str) -> None:
        self.page.locator(f'[data-test="remove-{slug(product_name)}"]').click()

    def cart_count(self) -> int:
        return int(self.cart_badge.inner_text()) if self.cart_badge.count() else 0

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
