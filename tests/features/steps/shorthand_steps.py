import time
from behave import given, when, then

from tests.pages.cases_pages import CasesPage
from tests.pages.auth_pages import AuthSignInPage, AuthAccountPage

# Steps for common sequences for reuse in different scenarios

@given('I\'m in firm "{firm}" as "{user_key}"')
def step_login_in_firm(context, firm: str, user_key: str):
    context.pages[AuthSignInPage].goto()
    username, password = context.pages[AuthSignInPage].get_user_credentials(user_key)
    context.pages[AuthSignInPage].action_login(username, password)
    context.pages[AuthAccountPage].check_url()
    if context.pages[AuthAccountPage].get_account_num() > 1:
        context.pages[AuthAccountPage].select_account_by_name(firm)
    context.pages[CasesPage].check_url()
    context.pages[CasesPage].goto() # Make sure we're not on triage for the next steps

# Helper for testing
@then("I wait for {seconds:d} seconds")
def step_wait_for_seconds(context, seconds: int):
    time.sleep(seconds)
