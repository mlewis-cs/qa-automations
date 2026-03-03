from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import sync_playwright
from os import getenv
import time

from tests.pages.auth_pages import AuthSignInPage, AuthAccountPage
from tests.pages.cases_pages import CasesPage, TriagePage

PRESENTATION_END_WAIT_SECONDS = 3

def _init_scenario_context(context):
    # New browser context per scenario to ensure a clean session.
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()
    # Load pages into context, accessed by class
    context.pages = {
        AuthSignInPage: AuthSignInPage(context.page),
        AuthAccountPage: AuthAccountPage(context.page),
        CasesPage: CasesPage(context.page),
        TriagePage: TriagePage(context.page),
    }


def before_all(context):
    # Load .env
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    presentation_mode = getenv("PRESENTATION_MODE") == "true"
    headless_mode = not presentation_mode
    context.presentation_mode = presentation_mode
    # Load browser
    context.pw = sync_playwright().start()
    context.browser = context.pw.chromium.launch(headless=headless_mode)


def before_scenario(context, scenario):
    # Ensure each scenario starts with a fresh session.
    _init_scenario_context(context)


def after_scenario(context, scenario):
    if getattr(context, "presentation_mode", False):
        time.sleep(PRESENTATION_END_WAIT_SECONDS)
    if getattr(context, "browser_context", None) is not None:
        context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.pw.stop()
