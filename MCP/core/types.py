from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import re
from typing import Any


SENSITIVE_KEYS = ("password", "token", "pin", "authorization")
REDACTED_VALUE = "***REDACTED***"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_sensitive_key(key: str) -> bool:
    lowered = key.lower()
    return any(token in lowered for token in SENSITIVE_KEYS)


def redact_string(value: str) -> str:
    redacted = value
    patterns = [
        r"(?i)(password=)([^&\s]+)",
        r"(?i)(token=)([^&\s]+)",
        r"(?i)(pin=)([^&\s]+)",
        r"(?i)(authorization:\s*bearer\s+)([^\s]+)",
    ]
    for pattern in patterns:
        redacted = re.sub(pattern, rf"\1{REDACTED_VALUE}", redacted)
    return redacted


def redact_payload(value: Any, key_hint: str = "") -> Any:
    if is_sensitive_key(key_hint):
        return REDACTED_VALUE
    if isinstance(value, dict):
        return {k: redact_payload(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_payload(item, key_hint) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_payload(item, key_hint) for item in value)
    if isinstance(value, str):
        return redact_string(value)
    return value


@dataclass
class StepLogRecord:
    id: int
    timestamp: str
    tool_name: str
    input: dict[str, Any]
    normalized_command: str
    result_summary: str
    status: str
    replayable: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CheckpointRecord:
    name: str
    created_at: str
    log_index: int
    session_name: str
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

