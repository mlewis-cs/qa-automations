from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from dotenv import load_dotenv

from .state_store import StateStore


PLAYWRIGHT_BIN = "/opt/homebrew/bin/playwright-cli"
ALLOWED_USER_COMMANDS = {"open", "goto", "snapshot", "run-code", "click", "fill", "wait"}


class PlaywrightRuntime:
    def __init__(self, store: StateStore):
        self.store = store
        self.session_name = self.store.session_name or "mcp-default"
        self.store.set_session_name(self.session_name)

        self.repo_root = Path(__file__).resolve().parents[2]
        self.base_url = ""
        self.is_initialized = False
        self.headless_override: bool | None = None
        self._load_env()

    def _load_env(self) -> None:
        env_path = self.repo_root / "tests" / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        self.base_url = os.getenv("BASE_URL", "").rstrip("/")

    def _default_signin_url(self) -> str:
        if not self.base_url:
            return "about:blank"
        return f"{self.base_url}/auth/signin"

    def _command_env(self) -> dict[str, str]:
        env = os.environ.copy()
        if self.headless_override is not None:
            env["HEADLESS_MODE"] = "true" if self.headless_override else "false"
        return env

    def _build_command(self, command: str, args: list[str]) -> list[str]:
        return [PLAYWRIGHT_BIN, f"-s={self.session_name}", command, *args]

    def _execute_cli_raw(
        self,
        command: str,
        args: list[str],
        timeout_seconds: int = 90,
    ) -> dict[str, Any]:
        command_vector = self._build_command(command, args)
        result = subprocess.run(
            command_vector,
            capture_output=True,
            text=True,
            env=self._command_env(),
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "command_vector": command_vector,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    def _parse_stdout(self, stdout: str) -> Any:
        if not stdout:
            return None
        candidates = [stdout]
        lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        candidates.extend(reversed(lines))
        for candidate in candidates:
            candidate = candidate.strip()
            if not candidate:
                continue
            try:
                return json.loads(candidate)
            except Exception:
                continue
        return stdout

    def _extract_first_url(self, text: str) -> str | None:
        match = re.search(r"https?://[^\s\"'`]+", text)
        return match.group(0) if match else None

    def _result_summary(self, response: dict[str, Any]) -> str:
        text = response.get("stdout") or response.get("stderr") or ""
        if len(text) > 280:
            return f"{text[:280]}..."
        return text

    def _raise_on_failure(self, response: dict[str, Any], command: str) -> None:
        if response["exit_code"] == 0:
            return
        stderr = response.get("stderr") or ""
        stdout = response.get("stdout") or ""
        details = stderr if stderr else stdout
        raise RuntimeError(f"playwright-cli {command} failed: {details}")

    def run_playwright_cli(
        self,
        command: str,
        args: list[str] | None = None,
        replayable: bool = False,
        log: bool = True,
        timeout_seconds: int = 90,
    ) -> dict[str, Any]:
        args = args or []
        if command not in ALLOWED_USER_COMMANDS:
            raise ValueError(
                f"Command '{command}' is not allowed. "
                f"Allowed commands: {sorted(ALLOWED_USER_COMMANDS)}"
            )

        response = self._execute_cli_raw(command=command, args=args, timeout_seconds=timeout_seconds)
        status = "SUCCESS" if response["exit_code"] == 0 else "FAILURE"
        normalized_command = " ".join(response["command_vector"])

        if log:
            self.store.append_log(
                tool_name="run_playwright_cli",
                input_data={
                    "command": command,
                    "args": args,
                    "replayable": replayable,
                    "timeout_seconds": timeout_seconds,
                },
                normalized_command=normalized_command,
                result_summary=self._result_summary(response),
                status=status,
                replayable=replayable and status == "SUCCESS",
            )

        self._raise_on_failure(response, command)
        response["parsed"] = self._parse_stdout(response["stdout"])
        return response

    def run_code(
        self,
        script: str,
        replayable: bool = False,
        log: bool = False,
        timeout_seconds: int = 90,
    ) -> dict[str, Any]:
        return self.run_playwright_cli(
            command="run-code",
            args=[script],
            replayable=replayable,
            log=log,
            timeout_seconds=timeout_seconds,
        )

    def get_current_url(self) -> str:
        response = self.run_code(
            "async (page) => page.url()",
            replayable=False,
            log=False,
            timeout_seconds=20,
        )
        parsed = response.get("parsed")
        if isinstance(parsed, str):
            parsed = parsed.strip().strip('"')
            extracted = self._extract_first_url(parsed)
            return extracted or parsed
        stdout = response.get("stdout", "")
        extracted = self._extract_first_url(stdout)
        return extracted or stdout.strip().strip('"')

    def _soft_reset_clear_storage(self) -> None:
        script = (
            "async (page) => {"
            " await page.context().clearCookies();"
            " await page.evaluate(async () => {"
            "   localStorage.clear();"
            "   sessionStorage.clear();"
            "   if (window.indexedDB && indexedDB.databases) {"
            "     const dbs = await indexedDB.databases();"
            "     await Promise.all(dbs.map((db) => new Promise((resolve) => {"
            "       if (!db.name) return resolve(null);"
            "       const req = indexedDB.deleteDatabase(db.name);"
            "       req.onsuccess = () => resolve(null);"
            "       req.onerror = () => resolve(null);"
            "       req.onblocked = () => resolve(null);"
            "     })));"
            "   }"
            " });"
            " await page.goto('about:blank', { waitUntil: 'domcontentloaded' });"
            " return page.url();"
            "}"
        )
        self.run_code(script, replayable=False, log=False, timeout_seconds=60)

    def run_premade_action(
        self,
        name: str,
        args: dict[str, Any] | None = None,
        log: bool = True,
        replayable: bool = True,
    ) -> dict[str, Any]:
        from MCP.services.actions import run_action

        args = args or {}
        status = "SUCCESS"
        result_summary = ""
        try:
            result = run_action(runtime=self, name=name, args=args)
            result_summary = json.dumps(result)[:280]
        except Exception as exc:
            status = "FAILURE"
            result_summary = str(exc)
            if log:
                self.store.append_log(
                    tool_name="run_premade_action",
                    input_data={"name": name, "args": args},
                    normalized_command=f"action:{name}",
                    result_summary=result_summary,
                    status=status,
                    replayable=False,
                )
            raise

        if log:
            self.store.append_log(
                tool_name="run_premade_action",
                input_data={"name": name, "args": args},
                normalized_command=f"action:{name}",
                result_summary=result_summary,
                status=status,
                replayable=replayable,
            )
        return result

    def run_profile(self, name: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
        from MCP.services.profiles import run_profile

        return run_profile(runtime=self, name=name, args=args or {})

    def replay_checkpoint(self, checkpoint_name: str) -> dict[str, Any]:
        checkpoint = self.store.get_checkpoint(checkpoint_name)
        if checkpoint is None:
            raise ValueError(f"Checkpoint '{checkpoint_name}' was not found.")

        replayed = 0
        skipped = 0
        for entry in self.store.get_log_slice(checkpoint["log_index"]):
            if not entry.get("replayable", False):
                skipped += 1
                continue

            tool_name = entry.get("tool_name")
            payload = entry.get("input", {})

            if tool_name == "run_premade_action":
                self.run_premade_action(
                    name=payload.get("name", ""),
                    args=payload.get("args", {}),
                    log=False,
                    replayable=True,
                )
                replayed += 1
            elif tool_name == "run_playwright_cli":
                self.run_playwright_cli(
                    command=payload.get("command", ""),
                    args=payload.get("args", []),
                    replayable=True,
                    log=False,
                    timeout_seconds=payload.get("timeout_seconds", 90),
                )
                replayed += 1
            else:
                skipped += 1

        return {
            "checkpoint": checkpoint_name,
            "checkpoint_log_index": checkpoint["log_index"],
            "replayed_steps": replayed,
            "skipped_steps": skipped,
        }

    def initialize_session(
        self,
        session_name: str | None = None,
        profile: str | None = None,
        checkpoint: str | None = None,
        reset_mode: str = "soft_clear_storage",
        headless: bool | None = None,
        replay: bool = True,
    ) -> dict[str, Any]:
        if reset_mode != "soft_clear_storage":
            raise ValueError(
                "Unsupported reset_mode. Use 'soft_clear_storage'."
            )

        if session_name and session_name != self.session_name:
            self.session_name = session_name
            self.store.set_session_name(session_name)
            self.is_initialized = False

        if headless is not None:
            self.headless_override = headless
        self.headless_override = False # <-- for testing ignore the previous lines and always set headless to false; comment this out l8r

        sequence: list[str] = []
        try:
            if not self.is_initialized:
                self.run_playwright_cli(
                    command="open",
                    args=[self._default_signin_url()],
                    replayable=False,
                    log=False,
                    timeout_seconds=90,
                )
                self.is_initialized = True
                sequence.append("open_session")
            else:
                self._soft_reset_clear_storage()
                sequence.append("soft_reset_clear_storage")

            profile_result = None
            if profile:
                profile_result = self.run_profile(profile)
                sequence.append(f"profile:{profile}")

            replay_result = None
            if checkpoint and replay:
                replay_result = self.replay_checkpoint(checkpoint)
                sequence.append(f"replay_checkpoint:{checkpoint}")

            result = {
                "status": "SUCCESS",
                "session_name": self.session_name,
                "reset_mode": reset_mode,
                "sequence": sequence,
                "profile_result": profile_result,
                "replay_result": replay_result,
                "current_url": self.get_current_url(),
                "headless": self.headless_override,
            }

            self.store.append_log(
                tool_name="initialize_session",
                input_data={
                    "session_name": session_name,
                    "profile": profile,
                    "checkpoint": checkpoint,
                    "reset_mode": reset_mode,
                    "headless": headless,
                    "replay": replay,
                },
                normalized_command=f"initialize_session:{self.session_name}",
                result_summary=json.dumps(
                    {"sequence": sequence, "current_url": result["current_url"]}
                ),
                status="SUCCESS",
                replayable=False,
            )
            return result
        except Exception as exc:
            self.store.append_log(
                tool_name="initialize_session",
                input_data={
                    "session_name": session_name,
                    "profile": profile,
                    "checkpoint": checkpoint,
                    "reset_mode": reset_mode,
                    "headless": headless,
                    "replay": replay,
                },
                normalized_command=f"initialize_session:{self.session_name}",
                result_summary=str(exc),
                status="FAILURE",
                replayable=False,
            )
            raise
