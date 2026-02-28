# QA Automations — Regression + Agentic UAT

This repo is a Playwright + Gherkin (Cucumber.js) regression and agentic UAT framework. It includes:
- A Playwright test harness in TypeScript
- Gherkin feature files + TypeScript step definitions
- An MCP server that exposes the current step inventory and feature catalog
- A Codex skill (`uat-scenario-writer`) that generates new scenarios and missing steps

## Goals
- Allow humans to describe tests in plain English
- Generate consistent Gherkin scenarios automatically
- Reuse existing step definitions where possible
- Flag missing steps with clear TODOs and explanations
- Provide a lightweight MCP surface for agentic test generation

## Architecture Overview

**Playwright + Cucumber.js**
- Playwright drives the browser
- Cucumber.js runs Gherkin features
- Steps are implemented in TypeScript

**MCP Server**
- Exposes existing steps and features to the Codex skill
- Enables scenario generation that respects existing test coverage

**Codex Skill**
- `uat-scenario-writer` uses MCP data to:
  - Create new `.feature` files
  - Reuse existing steps where possible
  - Insert missing steps with `# MUST IMPLEMENT`
  - Create step stubs in TypeScript with explanatory comments

## Repository Layout (Planned)

- `README.md`
- `package.json`
- `tsconfig.json`
- `playwright.config.ts`
- `cucumber.js`
- `features/`
- `features/<domain>/`
- `features/<domain>/<feature>.feature`
- `features/steps/`
- `features/steps/<domain>.steps.ts`
- `features/support/`
- `features/support/world.ts`
- `features/support/hooks.ts`
- `mcp/`
- `mcp/server.ts`
- `mcp/types.ts`
- `mcp/step-inventory.ts`
- `mcp/feature-index.ts`
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
   - Creates a TypeScript step stub in `features/steps/<domain>.steps.ts`
   - Annotates the stub with `// MUST IMPLEMENT: <reason>`
5. Adds a “Missing Steps Explanation” section to the end of the feature file.

### Example Missing Step (Feature File)
```gherkin
Scenario: Update profile picture
  Given I am on the profile page
  When I upload a new profile picture # MUST IMPLEMENT
  Then I should see the new profile picture
```

### Example Missing Step (Step Stub)
```ts
When('I upload a new profile picture', async function () {
  // MUST IMPLEMENT: No existing step handles file upload in profile context.
  throw new Error('Step not implemented');
});
```

## Environment Variables

- `BASE_URL`
  Base URL for the target staging environment.

## Running Tests (Planned)
- `npm test` or `npx cucumber-js`
- Playwright will launch browsers based on `playwright.config.ts`

## Next Steps
- Implement initial MCP server
- Add foundational step definitions
- Seed example feature files
- Run a first end-to-end regression pass
