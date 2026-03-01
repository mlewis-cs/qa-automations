import { Given, When, Then } from "@cucumber/cucumber";

Given("I am on the login page", async function () {
    await this.loginPage.goto();
});

When("I log in with username {string} and password {string}", async function (username: string, password: string) {
    await this.loginPage.login(username, password);
});