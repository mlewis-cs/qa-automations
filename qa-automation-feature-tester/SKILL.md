---
name: qa-automation-feature-tester
description: Plan and execute end-to-end feature validation with the qa_automation MCP, capture screenshot evidence, update MCP page/action coverage with selectors or routines discovered during exploration, and return a pass/fail report with embedded images. Use when asked to test a specific UI feature and provide proof of behavior.
---

# QA Automation Feature Tester

Execute this workflow when a user asks to test a feature and wants visual proof.

## Workflow

1. Define an evidence plan before running tests.
2. Execute tests using `qa_automation` MCP tools in the required order.
3. Expand MCP coverage in-repo for selectors/routines discovered during exploration.
4. Return a pass/fail report with embedded screenshots.

## Step 1: Build an Evidence Plan

Before any UI actions, write a short plan of what must be proven with screenshots.

Include at minimum:
- Primary success state (feature works as expected)
- Primary negative/empty state (feature returns no results or blocked/invalid state)
- Any critical edge state needed to claim confidence

For each planned screenshot, define:
- `id`: short key like `search_success`
- `purpose`: what behavior it proves
- `expected`: pass condition

Example for search:
- `search_success`: valid query returns expected rows/cards
- `search_no_results`: unmatched query shows no-results state

## Step 2: Execute via MCP (Required Order)

Always use this order unless blocked:

1. `qa_automation.initialize_session`
2. `qa_automation.get_page_context`
3. `qa_automation.run_premade_action` for known actions
4. `qa_automation.run_playwright_cli` only when needed for discovery/custom steps
5. `qa_automation.set_checkpoint` at meaningful milestones
6. `qa_automation.get_step_log` to summarize what was executed

Execution rules:
- Prefer headless unless user explicitly asks for headful.
- Prefer MCP actions/context over raw selectors.
- Mark direct CLI commands `replayable=true` only when deterministic.
- Capture screenshot files for each evidence item in the plan.

## Step 3: Codify Discoveries in Repo

If testing required off-guardrail CLI exploration, add stable discoveries back into MCP code:

- Add/adjust named selectors in `MCP/pages/<page>.py`.
- Add reusable action routines in `MCP/services/actions.py`.
- Add/init flows in `MCP/services/profiles.py` when setup is repeatedly needed.
- Update `MCP/pages/registry.py` when adding a new page context.

Only add stable selectors/flows that succeeded during execution.

## Step 4: Return a Report with Embedded Images

Return a compact report with:
- Feature under test
- Evidence summary (PASS/FAIL per evidence item)
- Key notes (unexpected behavior, flaky steps, assumptions)
- Embedded screenshots using markdown image syntax with absolute file paths
- Save screenshot files and other evidence in the folder `artifacts` in the repo.

Use this output shape:

```markdown
## Feature Test Report

- Feature: <name>
- Overall: PASS | FAIL

### Evidence
- PASS | FAIL: <evidence_id> - <what it proves>
- Expected: <expected behavior>
- Observed: <observed behavior>

![<evidence_id>](/absolute/path/to/image.png)

### Notes
- <important detail>
```

If any required evidence item fails, mark overall result as `FAIL`.
