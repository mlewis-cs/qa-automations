from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .types import CheckpointRecord, StepLogRecord, redact_payload, redact_string, utc_now_iso


class StateStore:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.state_dir = self.root_dir / ".state"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.state_dir / "session_state.json"
        self.checkpoints_file = self.state_dir / "checkpoints.json"

        self.session_name = "mcp-default"
        self.step_log: list[dict[str, Any]] = []
        self.next_id = 1
        self.checkpoints: dict[str, dict[str, Any]] = {}
        self._load()

    def _load_json_file(self, path: Path, default: dict[str, Any]) -> dict[str, Any]:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _save_json_file(self, path: Path, data: dict[str, Any]) -> None:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _load(self) -> None:
        session_data = self._load_json_file(
            self.session_file,
            {"session_name": "mcp-default", "step_log": [], "next_id": 1},
        )
        checkpoints_data = self._load_json_file(
            self.checkpoints_file,
            {"checkpoints": []},
        )

        self.session_name = session_data.get("session_name", "mcp-default")
        self.step_log = session_data.get("step_log", [])
        self.next_id = session_data.get("next_id", len(self.step_log) + 1)

        raw_checkpoints = checkpoints_data.get("checkpoints", [])
        self.checkpoints = {checkpoint["name"]: checkpoint for checkpoint in raw_checkpoints}

    def _persist_session(self) -> None:
        payload = {
            "session_name": self.session_name,
            "step_log": self.step_log,
            "next_id": self.next_id,
        }
        self._save_json_file(self.session_file, payload)

    def _persist_checkpoints(self) -> None:
        payload = {
            "checkpoints": sorted(
                self.checkpoints.values(),
                key=lambda checkpoint: checkpoint["created_at"],
            )
        }
        self._save_json_file(self.checkpoints_file, payload)

    def set_session_name(self, session_name: str) -> None:
        self.session_name = session_name
        self._persist_session()

    def append_log(
        self,
        tool_name: str,
        input_data: dict[str, Any],
        normalized_command: str,
        result_summary: str,
        status: str,
        replayable: bool,
    ) -> dict[str, Any]:
        record = StepLogRecord(
            id=self.next_id,
            timestamp=utc_now_iso(),
            tool_name=tool_name,
            input=redact_payload(input_data),
            normalized_command=redact_string(normalized_command),
            result_summary=redact_string(result_summary),
            status=status,
            replayable=replayable,
        )
        self.step_log.append(record.to_dict())
        self.next_id += 1
        self._persist_session()
        return record.to_dict()

    def get_step_log(self, limit: int | None = 200) -> list[dict[str, Any]]:
        if limit is None:
            return list(self.step_log)
        return self.step_log[-limit:]

    def get_log_slice(self, log_index: int) -> list[dict[str, Any]]:
        clamped = max(0, min(log_index, len(self.step_log)))
        return list(self.step_log[:clamped])

    def add_checkpoint(self, name: str, note: str | None = None) -> dict[str, Any]:
        if not name.strip():
            raise ValueError("Checkpoint name cannot be blank.")
        checkpoint = CheckpointRecord(
            name=name.strip(),
            created_at=utc_now_iso(),
            log_index=len(self.step_log),
            session_name=self.session_name,
            note=note,
        )
        self.checkpoints[checkpoint.name] = checkpoint.to_dict()
        self._persist_checkpoints()
        return checkpoint.to_dict()

    def list_checkpoints(self) -> list[dict[str, Any]]:
        return sorted(
            self.checkpoints.values(),
            key=lambda checkpoint: checkpoint["created_at"],
        )

    def get_checkpoint(self, name: str) -> dict[str, Any] | None:
        return self.checkpoints.get(name)

