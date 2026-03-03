from asyncio import sleep

from .page import BasePage


class CasesPage(BasePage):
    SUB_DIRECTORY = "/admin/cases"
