import { expect, test as base } from '@playwright/test';

import { setup, teardown } from './reset-fixture';

const COOKIE_CONSENT_NAMES = [
  'confirm_google',
  'confirm_cookies',
  'confirm_tracking',
  'confirm_facebook',
  'confirm_vimeo',
  'confirm_youtube',
];

type TestOptions = {
  cookieConsent: boolean;
};

type TestFixtures = {
  applyCookieConsent: void;
  resetBackend: void;
};

export const test = base.extend<TestOptions & TestFixtures>({
  cookieConsent: [true, { option: true }],
  applyCookieConsent: [
    async ({ baseURL, context, cookieConsent }, use) => {
      if (cookieConsent) {
        if (!baseURL) {
          throw new Error('Playwright baseURL is required for cookie consent');
        }
        await context.addCookies(
          COOKIE_CONSENT_NAMES.map((name) => ({
            name,
            value: '1',
            url: baseURL,
          })),
        );
      }
      await use();
    },
    { auto: true },
  ],
  resetBackend: [
    async ({ page, request }, use) => {
      await teardown(request);
      await setup(request);
      try {
        await use();
      } finally {
        await page.close().catch(() => {});
        await teardown(request);
      }
    },
    { auto: true },
  ],
});

export { expect };
