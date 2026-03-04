from behave import when, then
from urllib.parse import urlparse

from tests.pages.cases_pages import CasesPage, TriagePage


@when("I navigate to the triage page from cases")
def step_go_to_triage(context):
    context.pages[CasesPage].action_go_to_triage()
    context.pages[TriagePage].check_url()

@when("I go to the web app from cases")
def step_go_to_web_app(context):
    context.web_app_page = context.pages[CasesPage].action_go_to_web_app()

@then("I am redirected to the web app login page")
def step_on_web_app_login(context):
    expected_host = urlparse(CasesPage.WEB_APP_REDIRECT_URL).hostname

    parsed = urlparse(context.web_app_page.url)
    assert parsed.hostname == expected_host, (
        f"Expected web app host {expected_host}, but was {parsed.hostname}"
    )
    assert parsed.path.startswith("/login"), (
        f"Expected web app login path to start with /login, but was {parsed.path}"
    )


@when("I log out from the cases page")
def step_log_out_from_cases(context):
    context.pages[CasesPage].log_out()
