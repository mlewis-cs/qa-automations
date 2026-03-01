import { After, AfterAll, Before, BeforeAll, setDefaultTimeout } from "@cucumber/cucumber";
import { chromium, firefox, webkit, type Browser } from "@playwright/test";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import playwrightConfig from "../playwright.config.ts";
import type { World } from "./world.ts";

let browser: Browser | undefined;

setDefaultTimeout(60 * 1000);

BeforeAll(async () => {
    const headless = process.env.HEADLESS === "true";
    const preferred = (process.env.PW_BROWSER ?? "chromium").toLowerCase();
    const channel = process.env.PW_CHANNEL ?? "chrome";
    const pwHome = process.env.PW_HOME ?? path.join(process.cwd(), ".pw-home");
    await mkdir(pwHome, { recursive: true });
    const env = { ...process.env, HOME: pwHome };

    const order = preferred === "chromium"
        ? ["chromium", "webkit", "firefox"]
        : preferred === "webkit"
            ? ["webkit", "chromium", "firefox"]
            : ["firefox", "chromium", "webkit"];

    let lastError: unknown;
    for (const name of order) {
        try {
            if (name === "chromium") {
                browser = await chromium.launch({ headless, channel, env });
            } else if (name === "webkit") {
                browser = await webkit.launch({ headless, env });
            } else {
                browser = await firefox.launch({ headless, env });
            }
            return;
        } catch (err) {
            lastError = err;
        }
    }

    throw lastError;
});

Before(async function (this: World) {
    if (!browser) {
        throw new Error("Playwright browser not initialized");
    }
    const configuredBaseURL = typeof playwrightConfig?.projects?.[0]?.use?.baseURL === "string"
        ? playwrightConfig.projects[0].use.baseURL
        : undefined;
    const baseURL = process.env.BASE_URL ?? configuredBaseURL ?? "http://localhost:3000";
    this.context = await browser.newContext({ baseURL });
    this.page = await this.context.newPage();
});

After(async function (this: World) {
    await this.page?.close();
    await this.context?.close();
});

AfterAll(async () => {
    await browser?.close();
    browser = undefined;
});
