from .page import BasePage
from urllib.parse import urlparse


class CasesPage(BasePage):
    SUB_DIRECTORY = "/admin/cases"

    def check_url(self):
        # Some accounts land on sub-routes under /admin/ after login.
        self.page.wait_for_url("**/admin/**")
        path = urlparse(self.page.url).path
        assert path.startswith("/admin/"), f"Expected URL path to start with /admin/, but was {path}"
