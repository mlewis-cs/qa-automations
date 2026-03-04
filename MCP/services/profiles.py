from __future__ import annotations

from typing import Any, Callable


ProfileHandler = Callable[[Any, dict], dict]


def profile_signin_page(runtime: Any, args: dict) -> dict:
    goto_result = runtime.run_premade_action("goto_signin", args={}, log=True, replayable=True)
    return {
        "status": "SUCCESS",
        "profile": "signin_page",
        "steps": [goto_result],
    }


def profile_attorney_cases_view(runtime: Any, args: dict) -> dict:
    user_key = str(args.get("user_key", "single account attorney"))
    base_url = runtime.base_url
    if not base_url:
        raise ValueError("BASE_URL is missing. Set it in tests/.env")

    steps: list[dict] = []
    steps.append(runtime.run_premade_action("goto_signin", args={}, log=True, replayable=True))
    steps.append(runtime.run_premade_action("login", args={"user_key": user_key}, log=True, replayable=True))
    runtime.run_playwright_cli(
        command="goto",
        args=[f"{base_url}/admin/cases"],
        replayable=True,
        log=True,
    )
    steps.append({"status": "SUCCESS", "navigated_to": f"{base_url}/admin/cases"})

    return {
        "status": "SUCCESS",
        "profile": "attorney_cases_view",
        "user_key": user_key,
        "steps": steps,
    }


PROFILES: dict[str, ProfileHandler] = {
    "signin_page": profile_signin_page,
    "attorney_cases_view": profile_attorney_cases_view,
}


def list_profiles() -> list[str]:
    return sorted(PROFILES.keys())


def run_profile(runtime: Any, name: str, args: dict) -> dict:
    handler = PROFILES.get(name)
    if handler is None:
        available = ", ".join(list_profiles())
        raise ValueError(f"Unknown profile '{name}'. Available profiles: {available}")
    return handler(runtime, args)

