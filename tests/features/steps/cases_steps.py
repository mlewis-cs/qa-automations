from behave import when, then

from tests.pages.cases_pages import CasesPage, TriagePage


@when("I navigate to the triage page from cases")
def step_go_to_triage(context):
    context.pages[CasesPage].go_to_triage()
    context.pages[TriagePage].check_url()

@when("I go to the web app from cases")
def step_go_to_web_app(context):
    context.web_app_page = context.pages[CasesPage].go_to_web_app()

@then("I am redirected to the web app login page")
def step_on_web_app_login(context):
    context.pages[CasesPage].check_go_to_web_app_destination(context.web_app_page)


@when("I log out from the cases page")
def step_log_out_from_cases(context):
    context.pages[CasesPage].log_out()
