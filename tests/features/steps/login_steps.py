from behave import given, when, then
import re
from os import getenv
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from tests.pages.auth_pages import AuthSignInPage, AuthAccountPage
from tests.pages.cases_pages import CasesPage

@given("I am on the login page")
def step_open_login(context):
    context.pages[AuthSignInPage].goto()

@when('I log in as "{user_key}"')
def step_login_as_user(context, user_key: str):
    username, password = _get_user_credentials(user_key)
    context.pages[AuthSignInPage].login(username, password)

@given('I\'m in firm "{firm}" as "{user_key}"')
def step_login_in_firm(context, firm: str, user_key: str):
    context.pages[AuthSignInPage].goto()
    username, password = _get_user_credentials(user_key)
    context.pages[AuthSignInPage].login(username, password)

    destination = _wait_for_account_or_admin(context)
    if destination == "account":
        context.pages[AuthAccountPage].select_account_by_name(firm)
        context.pages[CasesPage].check_url()

@then("I am logged in after the account page")
def step_logged_in_after_account_page(context):
    context.pages[AuthAccountPage].check_url()
    assert context.pages[AuthAccountPage].check_account_num() == 1, "Expected user to have 1 account; update test data"
    context.pages[CasesPage].check_url()

@then("I am redirected to the account page")
def step_redirect_to_account(context):
    context.pages[AuthAccountPage].check_url()

@then("I am logged in")
def step_logged_in(context):
    context.pages[CasesPage].check_url()

@when("I select a random account")
def step_select_random_account(context):
    context.pages[AuthAccountPage].select_random_account()


def _normalize_user_key(user_key: str) -> str:
    # Allow behave steps to reference env vars with more natural formatting
    # ie "test attorney" -> TEST_ATTORNEY
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", user_key).strip("_")
    normalized = re.sub(r"_+", "_", normalized)
    return normalized.upper()


def _get_user_credentials(user_key: str) -> tuple[str, str]:
    normalized_key = _normalize_user_key(user_key)
    email_key = f"USER_{normalized_key}_EMAIL"
    password_key = f"USER_{normalized_key}_PASSWORD"

    username = getenv(email_key)
    password = getenv(password_key)
    if not username or not password:
        raise ValueError(
            f"{email_key} or {password_key} is not set in .env"
        )
    return username, password


def _wait_for_account_or_admin(context) -> str:
    try:
        context.page.wait_for_url("**/auth/account", timeout=5000)
        return "account"
    except PlaywrightTimeoutError:
        context.pages[CasesPage].check_url()
        return "admin"
