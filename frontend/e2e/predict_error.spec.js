import { test, expect } from '@playwright/test'

// Simulate backend 500 to ensure the UI surfaces the error message
test('backend 500 shows error message in UI', async ({ page }) => {
  await page.route('**/predict_temperature', route =>
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'server error' }),
    })
  )

  await page.goto('/')
  await page.fill('#humidity_pct', '55')
  await page.fill('#wind_speed', '12')
  await page.click('button[type=submit]')

  // the component catches the error and displays `Error: HTTP 500`
  await expect(page.locator('p').last()).toContainText('HTTP 500')
})
