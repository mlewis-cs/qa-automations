# Context

This is a regression testing suite built with Python, Behave, and Playwright

## Locations

* `.venv` is in the root
* feature files are in `tests/features/`
* `environment.py` is in `tests/features/`
* step definitions are in `tests/features/steps`
* page classes are in `tests/pages/`
* `.env` and `requirements.txt` are in `tests/`

## Architecture

* `environment.py` defines code to run before and after Behave events, mostly managing browser context. Here you can see `context.pages` be defined, any new page needs to be put in `context.pages` with the key being the class & the value being an instance of that class with `context.page` sent on init.
* Page classes define functions that can be done on each sub directory. Each page derives from `BasePage` in `page.py` which has helper functions that should always be checked for & used before defining custom logic. Each page class defines a constant `SUB_DIRECTORY` which tells you what it is mapped to. For example, if you are in a Playwright session and are in `{base_url}/auth/signin`, you can search in the repo for `"/auth/signin"` and find the logic for that page is in `auth_pages.py` in the class `AuthSignInPage`. From there you can see selectors & methods that can be called inside that page. Always check for the class assigned to the sub directory you're in before attempting to create new classes. Always use existing methods and selectors in that class before defining new ones.
* Step definitions should be short and simple, essentially acting as the "glue" between Behave steps and page classes. Aim to have step methods consist of calls to page class methods through `context.pages` and assertions. Always check for existing steps and try to re-use them before making new ones. Always check that the step signature isn't already defined somewhere else to avoid duplicates. Behave step definitions shouldn't require too many variables be put in; try to use context & helper functions where reasonable to keep behave step definitions simple; try to shield feature files from complexity.

## Answering Prompts

When answering prompts to add functionality, first use the repo as a reference of what pages / functionality exists, then use Playwright CLI to confirm selectors when needed. When using Playwright CLI, use .env credentials and BASE_URL to navigate initially, and search the repo by your sub directory to find the appropriate page class to find context in the repo.

## Verifying Answers

If you have created the necessary code to answer the prompt, always verify your steps. If the verification fails use the error message to adjust your approach and try again. You are only finished answering when you can get one of these testing options to pass.

1. If you have created a new test step, create a feature file in `tests/features/temporary/` that tests the new step and run it to verify it passes. Do not delete the file when you are done.
2. If you have modified existing behavior used by Behave tests, run feature files that use the modified code and verify it passes. If you need to add scenarios or modify one, use method 1 instead.

## Running Behave Steps

Use the project venv and point Behave at the feature file(s). If Playwright fails to launch in headful mode or with crashpad permission errors, run with headless mode and disable crash reporter:

```bash
env PW_DISABLE_CRASH_REPORTER=1 HEADLESS_MODE=true /.venv/bin/behave tests/features/login.feature
```

To run all features:

```bash
env PW_DISABLE_CRASH_REPORTER=1 HEADLESS_MODE=true /.venv/bin/behave tests/features
```
