from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from MCP.pages.registry import PAGE_CLASSES


def _match_page_by_path(path: str):
    matches = [
        page_cls for page_cls in PAGE_CLASSES
        if path.startswith(page_cls.SUB_DIRECTORY)
    ]
    if not matches:
        return None
    return sorted(matches, key=lambda page_cls: len(page_cls.SUB_DIRECTORY), reverse=True)[0]


def get_page_context(runtime: Any) -> dict[str, Any]:
    current_url = runtime.get_current_url()
    path = urlparse(current_url).path
    page_cls = _match_page_by_path(path)

    if page_cls is None:
        known_paths = [page.SUB_DIRECTORY for page in PAGE_CLASSES]
        return {
            "status": "FAILURE",
            "current_url": current_url,
            "path": path,
            "error": "No MCP page class mapping found for current path.",
            "known_sub_directories": sorted(known_paths),
        }

    return {
        "status": "SUCCESS",
        "current_url": current_url,
        "path": path,
        "page": {
            "name": page_cls.__name__,
            "sub_directory": page_cls.SUB_DIRECTORY,
            "selectors": page_cls.selectors(),
            "actions": page_cls.actions(),
            "checks": page_cls.checks(),
            "getters": page_cls.getters(),
        },
    }

