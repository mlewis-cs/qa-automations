from .page import BasePage
from urllib.parse import urlparse


class CasesPage(BasePage):
    SUB_DIRECTORY = "/admin/cases"
    WEB_APP_REDIRECT_URL = "https://sandbox.creativebriefcase.com/"
    # Selectors
    TRIAGE_BUTTON = "button:has-text('Triage')"
    GO_TO_WEB_APP_BUTTON = "[data-testid='sidebar-external-link-web_app']"
    AVATAR_BUTTON = "[data-testid='avatar']"
    LOGOUT_BUTTON = "text=Logout"

    def check_url(self):
        # Some accounts land on deeper /admin/ routes after login.
        self.page.wait_for_url("**/admin/**")
        path = urlparse(self.page.url).path
        assert path.startswith("/admin/"), f"Expected URL path to start with /admin/, but was {path}"

    def action_go_to_triage(self):
        self.click(self.TRIAGE_BUTTON)

    def action_go_to_web_app(self):
        # Capture web-app page that appears in new tab
        with self.page.context.expect_page() as new_page_info:
            self.click(self.GO_TO_WEB_APP_BUTTON)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    def open_profile_menu(self):
        logout = self.find(self.LOGOUT_BUTTON)
        for _ in range(3):
            self.click(self.AVATAR_BUTTON)
            try:
                logout.wait_for(state="visible", timeout=2000)
                return
            except Exception:
                continue
        raise AssertionError("Profile menu did not open after 3 attempts; Logout option was not visible")

    def log_out(self):
        self.open_profile_menu()
        self.click(self.LOGOUT_BUTTON)

class TriagePage(BasePage):
    SUB_DIRECTORY = "/admin/cases/triage"

    
