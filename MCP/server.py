"""
Minimal MCP server scaffold (no transport wired yet).

We'll add a transport (stdio/http) and tool handlers in follow-up steps.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ActionSpec:
    name: str
    description: str
    params: Dict[str, str]
    returns: Optional[str] = None


class McpServer:
    """Placeholder MCP server.

    TODO:
    - implement transport
    - register tools
    - connect to Playwright
    """

    def __init__(self) -> None:
        self.actions: Dict[str, ActionSpec] = {}

    def list_actions(self) -> List[ActionSpec]:
        return list(self.actions.values())

    def run_action(self, name: str, args: Dict[str, Any]) -> Any:
        raise NotImplementedError("run_action not wired yet")

    def run_cli(self, command: str) -> Any:
        raise NotImplementedError("run_cli not wired yet")


def main() -> None:
    # Placeholder entrypoint
    server = McpServer()
    print("MCP scaffold ready. No transport configured.")
    print(f"actions: {len(server.list_actions())}")


if __name__ == "__main__":
    main()
