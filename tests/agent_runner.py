import argparse
import json
import time
from os import getenv
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from tests.pages.auth_pages import AuthAccountPage, AuthSignInPage
from tests.pages.cases_pages import CasesPage


TASKS = {
    "login_single_account",
    "login_multi_account_random",
    "login_in_firm",
    "invalid_login",
    "back_to_login_from_account",
    "logout_from_cases",
    "go_to_web_app_from_cases",
}


def _bool_from_text(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


class AgentRunner:
    def __init__(self, headless: bool | None = None, generate_report: bool | None = None):
        env_path = Path(__file__).resolve().parent / ".env"
        load_dotenv(env_path)

        self.headless = (
            headless if headless is not None else _bool_from_text(getenv("HEADLESS_MODE")) or True
        )
        self.generate_report = (
            generate_report
            if generate_report is not None
            else _bool_from_text(getenv("GENERATE_REPORT")) or False
        )
        self.report_dir = Path(__file__).resolve().parents[1] / "report"

    def __enter__(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=self.headless)
        self.browser_context = self.browser.new_context()
        self.page = self.browser_context.new_page()
        self.pages = {
            AuthSignInPage: AuthSignInPage(self.page),
            AuthAccountPage: AuthAccountPage(self.page),
            CasesPage: CasesPage(self.page),
        }
        return self

    def __exit__(self, exc_type, exc, tb):
        if getattr(self, "browser_context", None) is not None:
            self.browser_context.close()
        if getattr(self, "browser", None) is not None:
            self.browser.close()
        if getattr(self, "pw", None) is not None:
            self.pw.stop()

    def _login_to_cases(
        self,
        user_key: str,
        firm: str | None = None,
        select_random: bool = False,
    ) -> dict[str, Any]:
        sign_in_page = self.pages[AuthSignInPage]
        account_page = self.pages[AuthAccountPage]
        cases_page = self.pages[CasesPage]

        sign_in_page.goto()
        username, password = sign_in_page.get_user_credentials(user_key)
        sign_in_page.action_login(username, password)

        account_page.check_url()
        account_count = account_page.get_account_num()
        if account_count > 1:
            if firm:
                account_page.select_account_by_name(firm)
            elif select_random:
                account_page.select_random_account()
            else:
                raise ValueError(
                    "Multiple accounts detected. Pass firm=<name> or set select_random=true."
                )

        cases_page.check_url()
        cases_page.goto()
        return {"account_count": account_count}

    def run(self, task: str, **kwargs) -> dict[str, Any]:
        if task not in TASKS:
            raise ValueError(f"Unknown task '{task}'. Use --list to see available tasks.")

        started = time.time()
        evidence: dict[str, Any] = {}
        error = None
        status = "SUCCESS"
        try:
            sign_in_page = self.pages[AuthSignInPage]
            account_page = self.pages[AuthAccountPage]
            cases_page = self.pages[CasesPage]

            if task == "login_single_account":
                user_key = kwargs.get("user_key", "single account attorney")
                sign_in_page.goto()
                username, password = sign_in_page.get_user_credentials(user_key)
                sign_in_page.action_login(username, password)
                account_page.check_url()
                account_count = account_page.get_account_num()
                assert account_count == 1, (
                    f"Expected one account for user '{user_key}', found {account_count}"
                )
                cases_page.check_url()
                evidence = {"account_count": account_count}

            elif task == "login_multi_account_random":
                user_key = kwargs.get("user_key", "multi account attorney")
                evidence = self._login_to_cases(user_key=user_key, select_random=True)

            elif task == "login_in_firm":
                user_key = kwargs.get("user_key", "multi account attorney")
                firm = kwargs.get("firm")
                if not firm:
                    raise ValueError("task=login_in_firm requires arg: firm=<firm name>")
                evidence = self._login_to_cases(user_key=user_key, firm=firm)

            elif task == "invalid_login":
                sign_in_page.goto()
                sign_in_page.action_login("invalid@example.com", "wrongpass")
                error_banner = sign_in_page.find(AuthSignInPage.INVALID_CREDENTIALS_ERROR)
                error_banner.wait_for(state="visible", timeout=5000)
                assert error_banner.is_visible(), "Expected invalid credentials error to be visible"
                sign_in_page.check_url()
                evidence = {"error_banner_visible": True}

            elif task == "back_to_login_from_account":
                user_key = kwargs.get("user_key", "multi account attorney")
                sign_in_page.goto()
                username, password = sign_in_page.get_user_credentials(user_key)
                sign_in_page.action_login(username, password)
                account_page.check_url()
                account_page.action_go_back_to_signin()
                sign_in_page.check_url()

            elif task == "logout_from_cases":
                user_key = kwargs.get("user_key", "single account attorney")
                firm = kwargs.get("firm")
                evidence = self._login_to_cases(user_key=user_key, firm=firm)
                cases_page.log_out()
                sign_in_page.check_url()

            elif task == "go_to_web_app_from_cases":
                user_key = kwargs.get("user_key", "single account attorney")
                firm = kwargs.get("firm")
                evidence = self._login_to_cases(user_key=user_key, firm=firm)
                web_app_page = cases_page.action_go_to_web_app()
                expected_host = urlparse(CasesPage.WEB_APP_REDIRECT_URL).hostname
                parsed = urlparse(web_app_page.url)
                assert parsed.hostname == expected_host, (
                    f"Expected web app host {expected_host}, but was {parsed.hostname}"
                )
                assert parsed.path.startswith("/login"), (
                    f"Expected web app login path to start with /login, but was {parsed.path}"
                )
                evidence["web_app_url"] = parsed._replace(query="", fragment="").geturl()
                web_app_page.close()

        except Exception as exc:  # noqa: BLE001
            status = "FAILURE"
            error = str(exc)

        duration_seconds = round(time.time() - started, 3)
        current_url = self.page.url if self.page else ""
        result = {
            "task": task,
            "status": status,
            "error": error,
            "duration_seconds": duration_seconds,
            "current_url": current_url,
            "evidence": evidence,
        }

        if self.generate_report:
            self.report_dir.mkdir(parents=True, exist_ok=True)
            screenshot_name = f"{task.lower()}-{status.lower()}.png"
            screenshot_path = self.report_dir / screenshot_name
            self.page.screenshot(path=str(screenshot_path), full_page=True)
            result["screenshot"] = str(screenshot_path)

        return result


def _parse_key_value_pairs(pairs: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid --arg value '{pair}'. Expected key=value.")
        key, value = pair.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run agent-focused Playwright tasks")
    parser.add_argument("task", nargs="?", help="Task name to run")
    parser.add_argument("--arg", action="append", default=[], help="Task arg in key=value form")
    parser.add_argument(
        "--headless",
        choices=["true", "false"],
        default=None,
        help="Override browser headless mode",
    )
    parser.add_argument(
        "--generate-report",
        choices=["true", "false"],
        default=None,
        help="Capture screenshot into report/ and include path in output",
    )
    parser.add_argument("--list", action="store_true", help="List available tasks")
    args = parser.parse_args()

    if args.list:
        print(json.dumps(sorted(TASKS), indent=2))
        return 0

    if not args.task:
        parser.error("task is required unless --list is used")

    task_args = _parse_key_value_pairs(args.arg)
    with AgentRunner(
        headless=_bool_from_text(args.headless),
        generate_report=_bool_from_text(args.generate_report),
    ) as runner:
        result = runner.run(args.task, **task_args)

    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
