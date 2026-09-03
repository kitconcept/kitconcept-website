import { defineConfig, devices } from '@playwright/test';

// Acceptance tests run against a Plone acceptance backend (RobotRemote enabled)
// and a running Volto frontend.
export default defineConfig({
  testDir: 'acceptance/tests',
  testMatch: ['**/*.{spec,test}.{ts,tsx}'],
  outputDir: 'acceptance/results',
  // Tests share a backend that is reset between tests.
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 3 : 0,
  timeout: 30_000,
  expect: {
    timeout: 10_000,
  },
  use: {
    baseURL: process.env.FRONTEND_URL || 'http://localhost:3000',
    browserName: 'chromium',
    viewport: { width: 1440, height: 1000 },
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1440, height: 1000 },
      },
    },
  ],
});
