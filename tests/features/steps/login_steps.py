from behave import given, when, then
from tests.pages.auth_pages import AuthSignInPage, AuthAccountPage
from tests.pages.cases_pages import CasesPage

@given("I am on the login page")
def step_open_login(context):
    context.pages[AuthSignInPage].goto()

@when('I log in as "{user_key}"')
def step_login_as_user(context, user_key: str):
    username, password = context.pages[AuthSignInPage].get_user_credentials(user_key)
    context.pages[AuthSignInPage].action_login(username, password)

@when("I log in with invalid credentials")
def step_login_with_invalid_credentials(context):
    context.pages[AuthSignInPage].action_login("invalid@example.com", "wrongpass")


@then("I am logged in after the account page")
def step_logged_in_after_account_page(context):
    context.pages[AuthAccountPage].check_url()
    assert context.pages[AuthAccountPage].get_account_num() == 1, "Expected user to have 1 account; update test data"
    context.pages[CasesPage].check_url()

@then("I am redirected to the account page")
def step_redirect_to_account(context):
    context.pages[AuthAccountPage].check_url()

@then("I am on the login page")
def step_on_login_page(context):
    context.pages[AuthSignInPage].check_url()

@then("I see an invalid credentials error message")
def step_invalid_credentials_error(context):
    error = context.pages[AuthSignInPage].find(AuthSignInPage.INVALID_CREDENTIALS_ERROR)
    error.wait_for(state="visible", timeout=5000)
    assert error.is_visible(), "Expected invalid credentials error message to be visible"

@then("I am logged in")
def step_logged_in(context):
    context.pages[CasesPage].check_url()

@when("I select a random account")
def step_select_random_account(context):
    context.pages[AuthAccountPage].select_random_account()

@when("I go back to the login page from the account page")
def step_go_back_to_login_from_account(context):
    context.pages[AuthAccountPage].action_go_back_to_signin()
