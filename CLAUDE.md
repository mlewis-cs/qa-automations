# Agent Instructions: `qa_automation` MCP Usage

This repo now supports an MCP server (`qa_automation`) for agent-driven Playwright testing.  
When the MCP is available, agents should use it as the primary interface for E2E execution.

## Goal

Run tests quickly in an interactive Playwright session using:
1. MCP prebuilt flows/context
2. MCP-backed direct Playwright CLI commands
3. Checkpoint/replay for fast iteration

## Required Tool Order

1. **Initialize session first**
   - Call `qa_automation.initialize_session`
   - Prefer a profile when possible (`signin_page`, `attorney_cases_view`)
   - Re-initialize mid-session to reset state without full browser relaunch

2. **Gather page context before exploratory actions**
   - Call `qa_automation.get_page_context`
   - Use returned selectors/actions/checks/getters from the mapped MCP page class

3. **Use pre-made actions before raw CLI**
   - Call `qa_automation.run_premade_action` when action exists (for consistency and replayability)
   - Current barebones actions: `goto_signin`, `login`, `assert_on_signin`

4. **Use direct CLI only when needed**
   - Call `qa_automation.run_playwright_cli` for discovery or missing actions
   - Allowed commands: `open`, `goto`, `snapshot`, `run-code`, `click`, `fill`, `wait`
   - Mark commands `replayable=true` only when deterministic/safe for replay

5. **Checkpoint long flows**
   - Call `qa_automation.set_checkpoint` after meaningful milestones
   - Use `initialize_session(..., checkpoint=..., replay=true)` to recover and iterate quickly
   - Inspect history with `qa_automation.get_step_log` and checkpoints with `qa_automation.list_checkpoints`

## Workflow Expectations

- Prefer MCP actions/context over hardcoded selectors.
- If `get_page_context` has no mapping, use CLI exploration and then add MCP-local page metadata under `MCP/pages`.
- Keep credentials out of logs and output.
- Default to headful unless a user explicitly asks for headless.
- On flaky behavior, reset via `initialize_session` and replay from checkpoint.

## Minimal Smoke Flow (Preferred Pattern)

1. `initialize_session(profile="signin_page")`
2. `get_page_context()`
3. `run_premade_action("login", {"user_key":"single account attorney"})`
4. `set_checkpoint("post-login")`
5. exploratory `run_playwright_cli(...)`
6. `initialize_session(checkpoint="post-login", replay=true)` to retry from known-good state
