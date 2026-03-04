# QA Automations

Agent-first end-to-end Playwright harness using page classes in `tests/pages/`.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r tests/requirements.txt
```

Populate `tests/.env` (see `tests/.env.example`) with:
- `BASE_URL`
- `HEADLESS_MODE`
- `GENERATE_REPORT`
- user credential pairs like `USER_SINGLE_ACCOUNT_ATTORNEY_EMAIL` / `..._PASSWORD`

## Run Tasks

List available tasks:

```bash
.venv/bin/python -m tests.agent_runner --list
```

Run a task:

```bash
env PW_DISABLE_CRASH_REPORTER=1 .venv/bin/python -m tests.agent_runner login_single_account
```

Run with explicit task args:

```bash
env PW_DISABLE_CRASH_REPORTER=1 .venv/bin/python -m tests.agent_runner login_in_firm --arg user_key="multi account attorney" --arg firm="Mobile Testing"
```

The runner prints JSON with task status, evidence, and errors for MCP/agent consumption.
