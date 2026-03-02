# QA Automations (Behave + Playwright) — Codebase Guide

This repo contains a small BDD-style UI test suite built on **Behave** and **Playwright (sync API)**. Tests live under `tests/` and are organized by feature files, step definitions, and page objects.

## Top-Level Layout

- `tests/features/*.feature`
  - Gherkin feature files describing scenarios.
- `tests/features/steps/*.py`
  - Behave step definitions that implement the Gherkin steps.
- `tests/features/environment.py`
  - Behave hooks that configure Playwright, load `.env`, and register page objects.
- `tests/pages/*.py`
  - Page objects used by steps.
- `tests/.env`
  - Runtime config (loaded by `environment.py`).
- `tests/.env.example`
  - Example values (includes `BASE_URL` and `HEADLESS_MODE`).
- `tests/requirements.txt`
  - Python dependencies: `behave`, `playwright`, `python-dotenv`.

## Current Test Architecture

**1) Feature files** (`tests/features/*.feature`)
- Define scenarios in Gherkin. Example: `tests/features/login.feature` has a `Login` feature with a `Valid login` scenario.

**2) Step definitions** (`tests/features/steps/*.py`)
- Implement Gherkin steps using Behave decorators (`@given`, `@when`, `@then`).
- Steps use:
  - `context.page` (Playwright `Page`) for direct actions and URL waits.
  - `context.pages[SomePageClass]` for page-object methods.
- Example: `tests/features/steps/login_steps.py` calls `context.pages[LoginPage].goto()` and `LoginPage.login()`.

**3) Environment setup** (`tests/features/environment.py`)
- `before_all`:
  - Loads `tests/.env` with `python-dotenv`.
  - Launches Playwright Chromium in headless or headed mode depending on `HEADLESS_MODE`.
  - Creates a single `Page` and registers page objects in `context.pages` (dictionary keyed by class).
- `after_all` closes the browser and Playwright instance.

**4) Page objects** (`tests/pages/*.py`)
- `BasePage` in `tests/pages/page.py` provides shared helpers (`goto`, `click`, `fill`).
- Each concrete page object inherits `BasePage` and **must** define `SUB_DIRECTORY`.
- Example: `LoginPage` in `tests/pages/login_page.py` sets `SUB_DIRECTORY = "/login"` and exposes a `login()` helper.

## Page Files and `SUB_DIRECTORY`

`BasePage.goto()` builds a URL like:

```
{BASE_URL.rstrip('/')}{SUB_DIRECTORY}
```

- `BASE_URL` comes from `tests/.env`.
- `SUB_DIRECTORY` is a required class attribute on every page object.
- `BasePage.__init_subclass__` enforces that `SUB_DIRECTORY` is non-empty, so missing values fail fast.

**How to use this when picking a page for a sub-directory:**
- Find (or create) a page class whose `SUB_DIRECTORY` matches the URL path you need.
- Call `context.pages[ThatPage].goto()` to navigate.

Example:
- `LoginPage.SUB_DIRECTORY = "/login"`
- `LoginPage.goto()` navigates to `BASE_URL + "/login"`.

## Adding or Updating Tests

**Add a new page object**
- Create a file in `tests/pages/`, inherit from `BasePage`, define `SUB_DIRECTORY`, add selectors and helper methods.
- Register the page in `tests/features/environment.py` by adding it to `context.pages`.

**Add a new step definition**
- Create or edit a file in `tests/features/steps/`.
- Use Behave decorators (`@given`, `@when`, `@then`).
- Use `context.pages[YourPage]` for page-level behavior, and `context.page` for low-level Playwright calls.

**Add a new feature**
- Add a new `.feature` file in `tests/features/`.
- Reference steps that exist or implement them in `tests/features/steps/`.

## Implementation Details That Matter

- **Playwright is used via the sync API**, not async.
- The login steps normalize user keys into env vars:
  - Step text: `Then I log in as "test attorney"`
  - Looks up `USER_TEST_ATTORNEY_EMAIL` and `USER_TEST_ATTORNEY_PASSWORD` in `.env`.
- `tests/features/steps/cases_steps.py` currently exists but is empty.

## Quick Mental Model for LLMs

- Feature files describe *what* should happen.
- Step definitions encode *how* to do it and orchestrate page objects.
- Page objects encapsulate selectors and page-specific actions.
- `SUB_DIRECTORY` is the canonical mapping from a page class to its URL path.
- `context.pages` is the registry that makes page objects available inside steps.
