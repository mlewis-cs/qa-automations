# Playwright QA MCP Harness

Agent-driven MCP server for on-the-fly Playwright testing with:
- persistent `playwright-cli` session management
- page-aware context discovery from MCP-local page classes
- pre-made actions and profiles
- direct Playwright CLI tool calls
- step logging and named checkpoints persisted in `MCP/.state/`

## Layout

- `MCP/server.py`: stdio MCP tool registration and entrypoint
- `MCP/core/runtime.py`: session lifecycle, CLI execution, reset/replay logic
- `MCP/core/state_store.py`: durable step logs and checkpoints
- `MCP/services/actions.py`: pre-made action handlers
- `MCP/services/profiles.py`: initialization profiles
- `MCP/services/page_context.py`: current URL -> page class context mapping
- `MCP/pages/`: MCP-focused page classes and selector/action/check metadata

## Install

```bash
.venv/bin/pip install -r MCP/requirements.txt
```

## Run (stdio MCP)

```bash
.venv/bin/python -m MCP.server
```

The server expects `tests/.env` to contain `BASE_URL` and credential keys used by actions:
- `USER_SINGLE_ACCOUNT_ATTORNEY_EMAIL`
- `USER_SINGLE_ACCOUNT_ATTORNEY_PASSWORD`
- `USER_MULTI_ACCOUNT_ATTORNEY_EMAIL`
- `USER_MULTI_ACCOUNT_ATTORNEY_PASSWORD`

## Tools

- `initialize_session(session_name?, profile?, checkpoint?, reset_mode?, headless?, replay?)`
- `get_page_context()`
- `run_premade_action(name, args?)`
- `run_playwright_cli(command, args?, replayable?)`
- `set_checkpoint(name, note?)`
- `list_checkpoints()`
- `get_step_log(limit?)`
- `list_capabilities()`

## Allowed Direct CLI Commands

`run_playwright_cli` enforces:
- `open`
- `goto`
- `snapshot`
- `run-code`
- `click`
- `fill`
- `wait`

## Reset and Replay Behavior

- First `initialize_session`: opens browser/session and navigates to signin URL.
- Mid-session `initialize_session`: clears cookies + storage and navigates to `about:blank` without restarting browser.
- If both `profile` and `checkpoint` are passed, sequence is:
  1. reset
  2. run profile
  3. replay replayable steps up to checkpoint index

## State Files

- `MCP/.state/session_state.json`
- `MCP/.state/checkpoints.json`
