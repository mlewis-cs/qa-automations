from __future__ import annotations

import re
from os import getenv

from .base_page import BasePage


class AuthSignInPage(BasePage):
    SUB_DIRECTORY = "/auth/signin"

    SELECTORS: dict[str, str] = {
        "email_phone": "#email",
        "password": "#password",
        "login_button": "button[type='submit']",
        "invalid_credentials_error": "h3:has-text('Your username and password combination is not correct. Please try again.')",
    }

    def action_login(self, username: str, password: str) -> None:
        """Metadata signature only; action execution is handled by MCP actions."""
        raise NotImplementedError

    def check_on_signin(self) -> None:
        """Metadata signature only; check execution is handled by MCP actions."""
        raise NotImplementedError

    @classmethod
    def get_user_credentials(cls, user_key: str) -> tuple[str, str]:
        normalized_key = cls._normalize_user_key(user_key)
        email_key = f"USER_{normalized_key}_EMAIL"
        password_key = f"USER_{normalized_key}_PASSWORD"

        username = getenv(email_key)
        password = getenv(password_key)
        if not username or not password:
            raise ValueError(
                f"{email_key} or {password_key} is not set in tests/.env"
            )
        return username, password

    @staticmethod
    def _normalize_user_key(user_key: str) -> str:
        normalized = re.sub(r"[^0-9A-Za-z]+", "_", user_key).strip("_")
        normalized = re.sub(r"_+", "_", normalized)
        return normalized.upper()

