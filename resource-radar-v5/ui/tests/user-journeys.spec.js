const { test, expect } = require('@playwright/test');

const BASE = process.env.RADAR_BASE_URL || 'http://127.0.0.1:4173/ui/';

test('novice can start from a need without knowing a product name', async ({ page }) => {
  await page.goto(BASE + '?fixture=1#radar');
  await expect(page.locator('.human-orientation-strip')).toContainText('un besoin');
  await page.locator('.human-orientation-strip a[href="#capabilities"]').click();
  await expect(page.locator('[data-view-panel="capabilities"] h1')).toContainText('écosystème');
});

test('configuration-first path is visible from the main radar', async ({ page }) => {
  await page.goto(BASE + '?fixture=1#radar');
  await page.locator('.human-orientation-strip a[href="#execution"]').click();
  await expect(page.locator('[data-view-panel="execution"]')).toBeVisible();
  await expect(page.locator('[data-view-panel="execution"]')).toContainText('Execution Estate');
  await expect(page.locator('[data-view-panel="execution"]')).toContainText('Workload');
  await expect(page.locator('[data-view-panel="execution"]')).toContainText('Execution Plan');
  await expect(page.locator('[data-view-panel="execution"]')).toContainText('Composer avant d’acheter');
});

test('a user can search a known resource and open its explanation', async ({ page }) => {
  await page.goto(BASE + '?fixture=1#radar');
  await page.locator('#radar-search').fill('Qdrant');
  await expect(page.locator('#result-count')).toContainText('1 ressource');
  await page.locator('tr[data-resource-id="db-qdrant"]').click();
  await expect(page).toHaveURL(/resource\.html\?/);
  await expect(page.locator('body')).toContainText('Qdrant');
  await expect(page.locator('body')).toContainText('30 secondes');
});

test('deprecated resource remains identifiable instead of looking recommended', async ({ page }) => {
  await page.goto(BASE + '?fixture=1#radar');
  await page.locator('#radar-search').fill('Flowise');
  const row = page.locator('tr[data-resource-id="workflow-flowise"]');
  await expect(row).toContainText('Déprécié');
});

test('expert evidence remains an explicit gate, not disguised public data', async ({ page }) => {
  await page.goto(BASE + '?fixture=1#expert-evidence');
  const panel = page.locator('[data-view-panel="expert-evidence"]');
  await expect(panel).toBeVisible();
  await expect(panel).toContainText(/Preuves|Evidence/);
  await expect(panel.locator('a[href*="premium"]')).toBeVisible();
});

test('mobile user can open navigation and reach configuration view', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(BASE + '?fixture=1#radar');
  await page.locator('#mobile-menu').click();
  await page.locator('[data-view="execution"]').click();
  await expect(page.locator('[data-view-panel="execution"]')).toBeVisible();
  await expect(page.locator('[data-view-panel="execution"] h1')).toContainText('disponible');
});

test('empty public projection does not invent recommendations', async ({ page }) => {
  await page.goto(BASE + '#radar');
  await expect(page.locator('#resource-empty')).toBeVisible();
  await expect(page.locator('#resource-empty')).toContainText(/Aucune donnée publique|Aucune ressource/);
});

test('keyboard shortcut sends a power user back to search', async ({ page }) => {
  await page.goto(BASE + '?fixture=1#execution');
  await page.keyboard.press('/');
  await expect(page.locator('[data-view-panel="radar"]')).toBeVisible();
  await expect(page.locator('#radar-search')).toBeFocused();
});
