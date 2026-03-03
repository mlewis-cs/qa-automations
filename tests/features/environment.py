from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import sync_playwright
from os import getenv
import time
import shutil

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
    generate_report = getenv("GENERATE_REPORT") == "true"
    headless_mode = not presentation_mode
    context.presentation_mode = presentation_mode
    context.generate_report = generate_report
    if presentation_mode:
        repo_root = Path(__file__).resolve().parents[2]
        report_dir = repo_root / "report"
        if report_dir.exists():
            shutil.rmtree(report_dir)
    # Load browser
    context.pw = sync_playwright().start()
    context.browser = context.pw.chromium.launch(headless=headless_mode)


def before_scenario(context, scenario):
    # Ensure each scenario starts with a fresh session.
    _init_scenario_context(context)


def after_scenario(context, scenario):
    if getattr(context, "presentation_mode", False):
        time.sleep(PRESENTATION_END_WAIT_SECONDS)
    
    if getattr(context, "page", None) is not None and getattr(context, "generate_report", False):
        repo_root = Path(__file__).resolve().parents[2]
        report_dir = repo_root / "report"
        report_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(
            c if c.isalnum() or c in ("-", "_") else "-" for c in scenario.name.strip().lower()
        ).strip("-")
        raw_status = getattr(scenario, "status", "")
        status_value = (
            getattr(raw_status, "name", None) or str(raw_status)
        ).lower()
        if "error" in status_value or "failed" in status_value:
            status_label = "FAILURE"
            suffix = "failed"
        else:
            status_label = "SUCCESS"
            suffix = "passed"
        screenshot_filename = f"{safe_name or 'scenario'}-{suffix}.png"
        screenshot_path = report_dir / screenshot_filename
        context.page.screenshot(path=str(screenshot_path), full_page=True)

        report_path = report_dir / "REPORT.md"
        relative_link = f"{screenshot_filename}"
        if not report_path.exists() or report_path.stat().st_size == 0:
            report_path.write_text("# REPORT\n\n", encoding="utf-8")
        with report_path.open("a", encoding="utf-8") as report_file:
            report_file.write(
                f"{status_label}: {scenario.name}\n"
                f"![{screenshot_filename}]({relative_link})\n\n"
            )
    
    if getattr(context, "browser_context", None) is not None:
        context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.pw.stop()
