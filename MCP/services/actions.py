from __future__ import annotations

import json
from typing import Any, Callable
from urllib.parse import urlparse

from MCP.pages.auth_signin_page import AuthSignInPage


ActionHandler = Callable[[Any, dict[str, Any]], dict[str, Any]]


def _required_base_url(runtime: Any) -> str:
    base_url = runtime.base_url
    if not base_url:
        raise ValueError("BASE_URL is missing. Set it in tests/.env")
    return base_url


def action_goto_signin(runtime: Any, args: dict[str, Any]) -> dict[str, Any]:
    base_url = _required_base_url(runtime)
    target = f"{base_url}{AuthSignInPage.SUB_DIRECTORY}"
    response = runtime.run_playwright_cli(
        command="goto",
        args=[target],
        replayable=True,
        log=False,
    )
    return {"status": "SUCCESS", "target_url": target, "stdout": response.get("stdout", "")}


def action_login(runtime: Any, args: dict[str, Any]) -> dict[str, Any]:
    user_key = str(args.get("user_key", "single account attorney"))
    username, password = AuthSignInPage.get_user_credentials(user_key)

    selectors = AuthSignInPage.SELECTORS
    script = (
        "async (page) => {"
        f"  await page.fill({json.dumps(selectors['email_phone'])}, {json.dumps(username)});"
        f"  await page.fill({json.dumps(selectors['password'])}, {json.dumps(password)});"
        f"  await page.click({json.dumps(selectors['login_button'])});"
        "  await page.waitForLoadState('domcontentloaded');"
        "  return page.url();"
        "}"
    )
    runtime.run_code(script=script, replayable=False, log=False, timeout_seconds=60)
    final_url = runtime.get_current_url()

    return {
        "status": "SUCCESS",
        "user_key": user_key,
        "final_url": final_url,
    }


def action_assert_on_signin(runtime: Any, args: dict[str, Any]) -> dict[str, Any]:
    current_url = runtime.get_current_url()
    expected_path = AuthSignInPage.SUB_DIRECTORY
    actual_path = urlparse(current_url).path
    if not actual_path.endswith(expected_path):
        raise AssertionError(
            f"Expected current path to end with {expected_path}, but found {actual_path}"
        )
    return {"status": "SUCCESS", "current_url": current_url}


ACTIONS: dict[str, ActionHandler] = {
    "goto_signin": action_goto_signin,
    "login": action_login,
    "assert_on_signin": action_assert_on_signin,
}


def list_actions() -> list[str]:
    return sorted(ACTIONS.keys())


def run_action(runtime: Any, name: str, args: dict[str, Any]) -> dict[str, Any]:
    handler = ACTIONS.get(name)
    if handler is None:
        available = ", ".join(list_actions())
        raise ValueError(f"Unknown action '{name}'. Available actions: {available}")
    return handler(runtime, args)
