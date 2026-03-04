from __future__ import annotations

from typing import Type

from .auth_signin_page import AuthSignInPage
from .base_page import BasePage


PAGE_CLASSES: list[Type[BasePage]] = [
    AuthSignInPage,
]

