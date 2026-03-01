import { test, expect } from '@playwright/test'

// See here how to get started:
// https://playwright.dev/docs/intro
test('visits the app root url', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('h1')).toHaveText('You did it!')
})

// end-to-end scenario around the weather form
// intercept the backend call so the test can run in isolation
// and ensure the component awaits the fetch result

test('submit weather form shows prediction', async ({ page }) => {
  await page.route('**/predict_temperature', route =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ predictions: [42] }),
    })
  )

  await page.goto('/')
  await page.fill('#humidity_pct', '55')
  await page.fill('#wind_speed', '12')
  await page.click('button[type=submit]')

  await expect(page.locator('p').last()).toContainText('42')
})
