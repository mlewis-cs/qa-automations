from random import randint
import re
from os import getenv
from .page import BasePage


class AuthSignInPage(BasePage):
    SUB_DIRECTORY = "/auth/signin"
    # Selectors
    EMAIL_PHONE = "#email"
    PASSWORD = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    INVALID_CREDENTIALS_ERROR = (
        "h3:has-text('Your username and password combination is not correct. Please try again.')"
    )

    def action_login(self, username: str, password: str):
        self.fill(self.EMAIL_PHONE, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_user_credentials(self, user_key: str) -> tuple[str, str]:
        normalized_key = self._normalize_user_key(user_key)
        email_key = f"USER_{normalized_key}_EMAIL"
        password_key = f"USER_{normalized_key}_PASSWORD"

        username = getenv(email_key)
        password = getenv(password_key)
        if not username or not password:
            raise ValueError(
                f"{email_key} or {password_key} is not set in .env"
            )
        return username, password

    @staticmethod
    def _normalize_user_key(user_key: str) -> str:
        normalized = re.sub(r"[^0-9A-Za-z]+", "_", user_key).strip("_")
        normalized = re.sub(r"_+", "_", normalized)
        return normalized.upper()


class AuthAccountPage(BasePage):
    SUB_DIRECTORY = "/auth/account"
    # Selectors
    BACK_TO_SIGNIN_BUTTON = "button:has-text('Back to Signin')"
    ACCOUNT_OPTIONS = "[data-testid^='sub-account-option']"


    def get_account_num(self) -> int:
        self.find(self.ACCOUNT_OPTIONS).first.wait_for(state="visible", timeout=5000)
        return self.find(self.ACCOUNT_OPTIONS).count()


    def select_random_account(self):
        accounts = self.find(self.ACCOUNT_OPTIONS)
        self.page.wait_for_function(
            """([selector, minimum]) => document.querySelectorAll(selector).length >= minimum""",
            arg=[self.ACCOUNT_OPTIONS, 2],
            timeout=5000,
        )
        count = accounts.count()
        if count <= 1:
            raise ValueError(f"Expected multiple accounts but found {count}; update test data")
        random_index = randint(0, count - 1)
        accounts.nth(random_index).click()


    def select_account_by_name(self, firm_name: str) -> None:
        accounts = self.find(self.ACCOUNT_OPTIONS)
        target = accounts.filter(has_text=firm_name).first
        target.wait_for(state="visible", timeout=5000)
        matches = accounts.filter(has_text=firm_name)
        count = matches.count()
        if count == 0:
            raise ValueError(f"Account named '{firm_name}' not found; update test data")
        if count > 1:
            raise ValueError(f"Multiple accounts named '{firm_name}' found; update test data")
        matches.first.click()


    def action_go_back_to_signin(self) -> None:
        self.click(self.BACK_TO_SIGNIN_BUTTON)
