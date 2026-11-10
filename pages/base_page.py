from playwright.sync_api import Page

from config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str = "/") -> None:
        self.page.goto(f"{BASE_URL}{path}")

    @property
    def url(self) -> str:
        return self.page.url
