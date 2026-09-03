import { expectNoAccessibilityViolations } from './accessibility';
import { expect, test } from './test';

test.describe('Homepage', () => {
  test('renders and has no automatic accessibility violations', async ({
    page,
  }) => {
    const response = await page.goto('/', { waitUntil: 'networkidle' });
    expect(response?.ok()).toBeTruthy();
    await expect(page.getByRole('banner')).toBeVisible();
    await expectNoAccessibilityViolations(page, {
      disabledRules: ['page-has-heading-one'],
    });
  });
});
