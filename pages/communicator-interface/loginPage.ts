import { Page } from "@playwright/test";

export class LoginPage {
    constructor(private page: Page) {}

    async goto() {
        await this.page.goto("/auth/signin");
    }

    async login(username: string, password: string) {
        const usernameInput = this.page
            .getByLabel(/email|username/i)
            .or(this.page.getByPlaceholder(/email|username/i))
            .or(this.page.locator('input[type="email"]'))
            .or(
                this.page.locator(
                    'input[name*="email" i], input[name*="user" i], input[id*="email" i], input[id*="user" i]'
                )
            )
            .first();

        const passwordInput = this.page
            .getByLabel(/password/i)
            .or(this.page.getByPlaceholder(/password/i))
            .or(this.page.locator('input[type="password"]'))
            .or(this.page.locator('input[name*="pass" i], input[id*="pass" i]'))
            .first();

        await usernameInput.fill(username);
        await passwordInput.fill(password);

        await this.page
            .getByRole("button", { name: /sign in|log in|login/i })
            .click();
    }
}
