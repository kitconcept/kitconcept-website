import type { Page } from '@playwright/test';

import { createContent } from './content';
import { login } from './login';
import { expect, test } from './test';

// A minimal valid 1x1 PNG, used as the Subsite logo.
const LOGO_PNG_BASE64 =
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';

/**
 * Returns the `src` of the header (banner) home logo currently rendered.
 * VLT renders the logo as an <img> inside the "Home" link of the header.
 */
async function headerLogoSrc(page: Page) {
  const logo = page
    .getByRole('banner')
    .getByRole('link', { name: 'Home' })
    .getByRole('img')
    .first();
  await expect(logo).toBeVisible();
  return logo.getAttribute('src');
}

test.describe('Subsite', () => {
  test('renders its own header/footer logo, scoped to the subsite navigation root', async ({
    page,
  }) => {
    await login(page);

    const subsiteId = `acceptance-subsite-${Date.now()}`;

    // A Subsite with its own logo, set on the shared VLT header behavior.
    await createContent(page, {
      contentType: 'Subsite',
      contentId: subsiteId,
      contentTitle: 'Acceptance Subsite',
      transition: 'publish',
      bodyModifier: (body) => ({
        ...body,
        logo: {
          'content-type': 'image/png',
          data: LOGO_PNG_BASE64,
          encoding: 'base64',
          filename: 'subsite-logo.png',
        },
        // Give the subsite a title block so its view renders a heading.
        blocks: {
          'd3f1c443-583f-4e8e-a682-3bf25752a300': { '@type': 'title' },
          '7624cf59-05d0-4055-8f55-5fd6597d84b0': { '@type': 'slate' },
        },
        blocks_layout: {
          items: [
            'd3f1c443-583f-4e8e-a682-3bf25752a300',
            '7624cf59-05d0-4055-8f55-5fd6597d84b0',
          ],
        },
      }),
    });

    // A page inside the subsite, to prove the logo is inherited by descendants.
    const childId = 'a-page';
    await createContent(page, {
      contentType: 'Document',
      contentId: childId,
      contentTitle: 'A Subsite Page',
      path: subsiteId,
      transition: 'publish',
    });

    // Baseline: the logo shown at the site root (not the subsite's).
    const siteRootResponse = await page.goto('/', { waitUntil: 'networkidle' });
    expect(siteRootResponse?.ok()).toBeTruthy();
    const siteRootLogo = await headerLogoSrc(page);

    // On the subsite itself, the header shows the subsite's own logo.
    const subsiteResponse = await page.goto(`/${subsiteId}`, {
      waitUntil: 'networkidle',
    });
    expect(subsiteResponse?.ok()).toBeTruthy();
    await expect(
      page.getByRole('heading', { name: 'Acceptance Subsite' }),
    ).toBeVisible();
    const subsiteLogo = await headerLogoSrc(page);

    // The subsite logo is its own, distinct from the site root logo. This is
    // what proves the header resolves the logo from the nearest navigation
    // root rather than always from the site root.
    expect(subsiteLogo).toBeTruthy();
    expect(subsiteLogo).not.toBe(siteRootLogo);

    // A descendant page inherits the subsite's logo (nearest navigation root).
    const childResponse = await page.goto(`/${subsiteId}/${childId}`, {
      waitUntil: 'networkidle',
    });
    expect(childResponse?.ok()).toBeTruthy();
    await expect(
      page.getByRole('heading', { name: 'A Subsite Page' }),
    ).toBeVisible();
    const childLogo = await headerLogoSrc(page);

    expect(childLogo).toBe(subsiteLogo);
  });
});
