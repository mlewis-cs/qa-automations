from behave import given, when, then
import re
from tests.pages.login_page import LoginPage
from os import getenv

@given("I am on the login page")
def step_open_login(context):
    context.pages[LoginPage].goto()
    context.page.wait_for_url("**/login")
    assert context.page.url.endswith("/login"), f"Expected to be on login page, but was on {context.page.url}"

@then('I log in as "{user_key}"')
def step_login_as_user(context, user_key: str):
    normalized_key = _normalize_user_key(user_key)
    email_key = f"USER_{normalized_key}_EMAIL"
    password_key = f"USER_{normalized_key}_PASSWORD"

    username = getenv(email_key)
    password = getenv(password_key)
    if not username or not password:
        raise ValueError(
            f"{email_key} or {password_key} is not set in .env"
        )
    context.pages[LoginPage].login(username, password)

@then ("I should see the cases page")
def step_see_cases(context):
    context.page.wait_for_url("**/cases")
    assert context.page.url.endswith("/cases"), f"Expected to be on cases page, but was on {context.page.url}"


def _normalize_user_key(user_key: str) -> str:
    # Allow behave steps to reference env vars with more natural formatting
    # ie "test attorney" -> TEST_ATTORNEY
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", user_key).strip("_")
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.upper()