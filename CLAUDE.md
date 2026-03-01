# QA Automations — Regression + Agentic UAT

This repo is a Playwright + Gherkin (Behave) regression and agentic UAT framework. It includes:
- A Playwright test harness in Python
- Gherkin feature files + Python step definitions
- An MCP server that exposes the current step inventory and feature catalog (planned)
- A Codex skill (`uat-scenario-writer`) that generates new scenarios and missing steps (planned)

## Goals
- Allow humans to describe tests in plain English
- Generate consistent Gherkin scenarios automatically
- Reuse existing step definitions where possible
- Flag missing steps with clear TODOs and explanations
- Provide a lightweight MCP surface for agentic test generation

## Architecture Overview

**Playwright + Behave**
- Playwright drives the browser
- Behave runs Gherkin features
- Steps are implemented in Python

**MCP Server**
- Exposes existing steps and features to the Codex skill
- Enables scenario generation that respects existing test coverage

**Codex Skill**
- `uat-scenario-writer` uses MCP data to:
  - Create new `.feature` files
  - Reuse existing steps where possible
  - Insert missing steps with `# MUST IMPLEMENT`
  - Create step stubs in Python with explanatory comments

## Repository Layout (Planned)

- `README.md`
- `requirements.txt`
- `behave.ini`
- `features/`
- `features/<domain>/`
- `features/<domain>/<feature>.feature`
- `features/steps/`
- `features/steps/<domain>_steps.py`
- `features/environment.py`
- `mcp/`
- `mcp/server.py`
- `mcp/types.py`
- `mcp/step_inventory.py`
- `mcp/feature_index.py`
- `mcp/README.md`
- `skills/`
- `skills/uat-scenario-writer/`
- `skills/uat-scenario-writer/SKILL.md`
- `skills/uat-scenario-writer/templates/`
- `skills/uat-scenario-writer/templates/feature.md`
- `skills/uat-scenario-writer/templates/step-stub.ts`

## MCP API (v1)

The MCP exposes a minimal set of endpoints for scenario generation:

- `GET /steps`
  - Returns step inventory (Given/When/Then patterns + location)
- `GET /features`
  - Returns existing features and scenario titles
- `GET /health`
  - Health check for the MCP server

## How the Skill Generates Scenarios

The `uat-scenario-writer` skill:
1. Reads MCP `steps` and `features`.
2. Produces a new `.feature` file in `features/<domain>/`.
3. Reuses existing steps whenever possible.
4. If a step is missing:
   - Adds `# MUST IMPLEMENT` to the step line in the `.feature`
   - Creates a Python step stub in `features/steps/<domain>_steps.py`
   - Annotates the stub with `# MUST IMPLEMENT: <reason>`
5. Adds a “Missing Steps Explanation” section to the end of the feature file.

### Example Missing Step (Feature File)
```gherkin
Scenario: Update profile picture
  Given I am on the profile page
  When I upload a new profile picture # MUST IMPLEMENT
  Then I should see the new profile picture
```

### Example Missing Step (Step Stub)
```py
@when("I upload a new profile picture")
def step_when_upload_profile_picture(context):
  # MUST IMPLEMENT: No existing step handles file upload in profile context.
  raise NotImplementedError("Step not implemented")
```

## Environment Variables

- `BASE_URL`
  Base URL for the target staging environment.

## Running Tests (Planned)
- `python -m behave` (run from `tests/`)
- Playwright will launch browsers based on environment variables

## Next Steps
- Implement initial MCP server
- Add foundational step definitions
- Seed example feature files
- Run a first end-to-end regression pass
