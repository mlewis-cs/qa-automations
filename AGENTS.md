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
