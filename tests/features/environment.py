from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import sync_playwright
from os import getenv

from tests.pages.login_page import LoginPage


def before_all(context):
    # Load .env
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)
    headless_mode = getenv("HEADLESS_MODE") == "true"
    # Load browser
    context.pw = sync_playwright().start()
    context.browser = context.pw.chromium.launch(headless=headless_mode)
    context.page = context.browser.new_page()
    # Load pages into context, accessed by class
    context.pages = {
        LoginPage: LoginPage(context.page),
    }


def after_all(context):
    context.browser.close()
    context.pw.stop()
