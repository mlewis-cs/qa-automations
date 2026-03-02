from playwright.sync_api import Page
from os import getenv


class BasePage:
    SUB_DIRECTORY: str = ""

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not cls.SUB_DIRECTORY:
            raise NotImplementedError(f"SUB_DIRECTORY must be defined in {cls.__name__}")


    def __init__(self, page: Page):
        self.page = page
    
    # Helper functions

    def goto(self):
        base_url = getenv("BASE_URL")
        if not base_url:
            raise ValueError("BASE_URL environment variable is not set. Add it to tests/.env")
        url = f"{base_url.rstrip('/')}{self.SUB_DIRECTORY}"
        self.page.goto(url, wait_until="domcontentloaded")


    def click(self, selector: str) -> None:
        self.page.locator(selector).click()
    

    def fill(self, selector: str, text: str) -> None:
        self.page.locator(selector).fill(text)