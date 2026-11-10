from pages.base_page import BasePage
from utils.helpers import slug


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.items = page.locator('[data-test="inventory-item"]')
        self.names = page.locator('[data-test="inventory-item-name"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def item_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def remove(self, product_name: str) -> None:
        self.page.locator(f'[data-test="remove-{slug(product_name)}"]').click()

    def checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
