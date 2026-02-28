import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  projects: [
    {
      name: "communicator-interface",
      testDir: "./tests/communicator-interface",
      use: {
        baseURL: "https://chrome.casestatus.com"
      }
    },
  ]
});
