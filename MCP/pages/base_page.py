from __future__ import annotations

import inspect
from typing import Any


class BasePage:
    SUB_DIRECTORY: str = ""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if not cls.SUB_DIRECTORY:
            raise NotImplementedError(f"SUB_DIRECTORY must be defined in {cls.__name__}")

    @classmethod
    def selectors(cls) -> dict[str, str]:
        selected: dict[str, str] = {}
        for attr in dir(cls):
            if not attr.isupper():
                continue
            value = getattr(cls, attr)
            if isinstance(value, str):
                selected[attr] = value
        return selected

    @classmethod
    def _collect_methods(cls, prefix: str) -> list[dict[str, Any]]:
        methods: list[dict[str, Any]] = []
        for attr in dir(cls):
            if not attr.startswith(prefix):
                continue
            member = getattr(cls, attr)
            if not callable(member):
                continue
            signature = inspect.signature(member)
            params = [
                name for name in signature.parameters
                if name != "self" and name != "cls"
            ]
            methods.append({"name": attr, "params": params})
        return sorted(methods, key=lambda item: item["name"])

    @classmethod
    def actions(cls) -> list[dict[str, Any]]:
        return cls._collect_methods("action_")

    @classmethod
    def checks(cls) -> list[dict[str, Any]]:
        return cls._collect_methods("check_")

    @classmethod
    def getters(cls) -> list[dict[str, Any]]:
        return cls._collect_methods("get_")

