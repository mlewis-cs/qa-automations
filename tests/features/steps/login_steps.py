from behave import given, when, then
import re
from tests.pages.auth_pages import AuthSignInPage, AuthAccountPage
from tests.pages.cases_page import CasesPage
from os import getenv

@given("I am on the login page")
def step_open_login(context):
    context.pages[AuthSignInPage].goto()

@when('I log in as "{user_key}"')
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
    context.pages[AuthSignInPage].login(username, password)

@then("I am redirected to the cases page after the account page")
def step_redirect_account_to_cases(context):
    context.pages[AuthAccountPage].check_url()
    assert context.pages[AuthAccountPage].check_account_num() == 1, "Expected user to have 1 account; update test data"
    context.pages[CasesPage].check_url()

@then("I am redirected to the account page")
def step_redirect_to_account(context):
    context.pages[AuthAccountPage].check_url()

@then("I am redirected to the cases page")
def step_redirect_to_cases(context):
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
