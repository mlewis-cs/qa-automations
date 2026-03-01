import { setWorldConstructor } from "@cucumber/cucumber";
import type { BrowserContext, Page } from "@playwright/test";
import { LoginPage } from "./communicator-interface/loginPage.ts";

export class World {
    page!: Page;
    context?: BrowserContext;

    private _loginPage?: LoginPage;

    get loginPage() {
        this._loginPage ??= new LoginPage(this.page);
        return this._loginPage;
    }
}

setWorldConstructor(World);
