from random import randint
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

    def login(self, username: str, password: str):
        self.fill(self.EMAIL_PHONE, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def check_invalid_credentials_error(self) -> None:
        error = self.find(self.INVALID_CREDENTIALS_ERROR)
        error.wait_for(state="visible", timeout=5000)


class AuthAccountPage(BasePage):
    SUB_DIRECTORY = "/auth/account"
    # Selectors
    BACK_TO_SIGNIN_BUTTON = "button:has-text('Back to Signin')"

    def check_account_num(self) -> int:
        return self.find("[data-testid^='sub-account-option']").count()


    def select_random_account(self):
        accounts = self.find("[data-testid^='sub-account-option']")
        count = accounts.count()
        if count <= 1:
            raise ValueError(f"Expected multiple accounts but found {count}; update test data")
        random_index = randint(0, count - 1)
        accounts.nth(random_index).click()


    def select_account_by_name(self, firm_name: str) -> None:
        accounts = self.find("[data-testid^='sub-account-option']")
        matches = accounts.filter(has_text=firm_name)
        count = matches.count()
        if count == 0:
            raise ValueError(f"Account named '{firm_name}' not found; update test data")
        if count > 1:
            raise ValueError(f"Multiple accounts named '{firm_name}' found; update test data")
        matches.first.click()

    def go_back_to_signin(self) -> None:
        self.click(self.BACK_TO_SIGNIN_BUTTON)
