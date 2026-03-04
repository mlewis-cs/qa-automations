from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from MCP.core.runtime import PlaywrightRuntime
from MCP.core.state_store import StateStore
from MCP.services.actions import list_actions
from MCP.services.page_context import get_page_context as resolve_page_context
from MCP.services.profiles import list_profiles


mcp = FastMCP("qa-playwright-harness")
store = StateStore(Path(__file__).resolve().parent)
runtime = PlaywrightRuntime(store=store)


def _safe_tool_call(callback):
    try:
        return callback()
    except Exception as exc:  # noqa: BLE001
        return {"status": "FAILURE", "error": str(exc)}


@mcp.tool()
def initialize_session(
    session_name: str | None = None,
    profile: str | None = None,
    checkpoint: str | None = None,
    reset_mode: str = "soft_clear_storage",
    headless: bool | None = None,
    replay: bool = True,
) -> dict[str, Any]:
    """Initialize or reset the active Playwright CLI session."""

    return _safe_tool_call(
        lambda: runtime.initialize_session(
            session_name=session_name,
            profile=profile,
            checkpoint=checkpoint,
            reset_mode=reset_mode,
            headless=headless,
            replay=replay,
        )
    )


@mcp.tool()
def get_page_context() -> dict[str, Any]:
    """Get selectors/actions/checks/getters from the MCP page class for current URL."""

    return _safe_tool_call(lambda: resolve_page_context(runtime))


@mcp.tool()
def run_premade_action(name: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run a named MCP pre-made action and return control to the agent."""

    return _safe_tool_call(
        lambda: {
            "status": "SUCCESS",
            "action": name,
            "result": runtime.run_premade_action(name=name, args=args or {}, log=True),
        }
    )


@mcp.tool()
def run_playwright_cli(
    command: str,
    args: list[str] | None = None,
    replayable: bool = False,
) -> dict[str, Any]:
    """Run an allowed Playwright CLI command directly."""

    return _safe_tool_call(
        lambda: {
            "status": "SUCCESS",
            "result": runtime.run_playwright_cli(
                command=command,
                args=args or [],
                replayable=replayable,
                log=True,
            ),
        }
    )


@mcp.tool()
def set_checkpoint(name: str, note: str | None = None) -> dict[str, Any]:
    """Save a named checkpoint at current step-log index."""

    return _safe_tool_call(
        lambda: {
            "status": "SUCCESS",
            "checkpoint": store.add_checkpoint(name=name, note=note),
        }
    )


@mcp.tool()
def list_checkpoints() -> dict[str, Any]:
    """List all named checkpoints."""

    return _safe_tool_call(
        lambda: {"status": "SUCCESS", "checkpoints": store.list_checkpoints()}
    )


@mcp.tool()
def get_step_log(limit: int = 200) -> dict[str, Any]:
    """Get recently logged MCP operations."""

    return _safe_tool_call(
        lambda: {
            "status": "SUCCESS",
            "step_log": store.get_step_log(limit=limit),
        }
    )


@mcp.tool()
def list_capabilities() -> dict[str, Any]:
    """List available profiles and actions."""

    return {
        "status": "SUCCESS",
        "profiles": list_profiles(),
        "actions": list_actions(),
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
