from __future__ import annotations

from .base_page import BasePage


class CasesTriagePage(BasePage):
    SUB_DIRECTORY = "/admin/cases/triage"

    SELECTORS: dict[str, str] = {
        "active_tab": "a[href*='/admin/cases/triage/active']",
        "snoozed_tab": "a[href*='/admin/cases/triage/snoozed']",
        "resolved_tab": "a[href*='/admin/cases/triage/resolved']",
        "my_cases_filter": "input[name='my_cases']",
    }

    def action_open_tab(self, tab: str) -> None:
        """Metadata signature only; action execution is handled by MCP actions."""
        raise NotImplementedError

    def check_tab_present(self, tab: str) -> None:
        """Metadata signature only; check execution is handled by MCP checks."""
        raise NotImplementedError

    def get_tab_hrefs(self) -> None:
        """Metadata signature only; getter execution is handled by MCP runtime."""
        raise NotImplementedError
