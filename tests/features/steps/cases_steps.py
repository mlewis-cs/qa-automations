from behave import when

from tests.pages.cases_pages import CasesPage, TriagePage


@when("I navigate to the triage page from cases")
def step_go_to_triage(context):
    context.pages[CasesPage].go_to_triage()
    context.pages[TriagePage].check_url()
