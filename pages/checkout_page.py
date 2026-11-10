from pages.base_page import BasePage
from utils.helpers import money


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.error = page.locator('[data-test="error"]')
        self.subtotal_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.complete_header = page.locator('[data-test="complete-header"]')

    def fill_info(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_(self) -> None:
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    def error_text(self) -> str:
        return self.error.inner_text()

    def subtotal(self) -> float:
        return money(self.subtotal_label.inner_text())

    def tax(self) -> float:
        return money(self.tax_label.inner_text())

    def total(self) -> float:
        return money(self.total_label.inner_text())
