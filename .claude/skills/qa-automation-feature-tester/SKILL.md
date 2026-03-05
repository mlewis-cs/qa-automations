---
name: qa-automation-feature-tester
description: Plan and execute end-to-end feature validation with the qa_automation MCP, capture screenshot evidence, update MCP page/action coverage with selectors or routines discovered during exploration, and return a pass/fail report with embedded images. Use when asked to test a specific UI feature and provide proof of behavior.
---

# QA Automation Feature Tester

Test a feature end-to-end using the `qa_automation` MCP, capture visual evidence, and return a pass/fail report with screenshots.

## Workflow

### 1. Plan Evidence

Before running tests, outline what must be proven:
- **Success state**: feature works as expected
- **Empty/negative state**: no results or blocked state
- **Edge cases**: any critical conditions needed for confidence

For each screenshot, define: `id` (short key), `purpose` (what it proves), `expected` (pass condition).

Example for search:
```
- search_success: valid query returns expected rows
- search_no_results: unmatched query shows empty state
```

### 2. Execute Tests via MCP

Follow this order (from CLAUDE.md):

1. `qa_automation.initialize_session` — start browser (use profile if available)
2. `qa_automation.get_page_context` — get available selectors/actions
3. `qa_automation.run_premade_action` — use built-in actions when possible
4. `qa_automation.run_playwright_cli` — CLI exploration only when needed (mark `replayable=true` if deterministic)
5. `qa_automation.set_checkpoint` — save state at milestones for fast replay
6. Capture screenshots for each evidence item

Keep execution headless unless user asks otherwise. Prefer MCP actions over raw selectors.

### 3. Add Discoveries to MCP

If exploration found stable selectors/flows, add them back to the codebase:

- **New selectors**: `MCP/pages/<page>.py`
- **Reusable actions**: `MCP/services/actions.py`
- **Setup flows**: `MCP/services/profiles.py`
- **New pages**: `MCP/pages/registry.py`

Only commit stable discoveries that succeeded during testing.

### 4. Report Results

Return a compact report with embedded screenshots:

```markdown
## Feature Test Report

**Feature**: <name>
**Result**: PASS | FAIL

### Evidence
- PASS/FAIL: `evidence_id` — what it proves
  - Expected: <behavior>
  - Observed: <behavior>

![evidence_id](/absolute/path/to/screenshot.png)

### Notes
- <unexpected behavior or flaky steps>
```

Save screenshots in `artifacts/` and use absolute file paths in markdown. Mark overall FAIL if any required evidence fails.
