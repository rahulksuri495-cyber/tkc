import { expect, test, type Page } from "@playwright/test";

const breakpoints = [
  { name: "mobile", width: 390, height: 844 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1280, height: 800 },
] as const;

const tamannaahGalleryFiles = [
  "tamannaah-dark-dress.jpg",
  "tamannaah-gold-yacht.jpg",
  "tamannaah-red-portrait.jpg",
  "tamannaah-tkctalent.jpg",
];

async function assertImagesDecoded(page: Page, selector: string, minimum: number) {
  await page.waitForSelector(selector);
  await expect.poll(() => page.locator(selector).evaluateAll((images) =>
    images.filter((node) => {
      const image = node as HTMLImageElement;
      return image.complete && image.naturalWidth > 0 && image.naturalHeight > 0;
    }).length,
  )).toBeGreaterThanOrEqual(minimum);
}

async function assertAtLeastOnePaintedImage(page: Page, selector: string) {
  const painted = await page.locator(selector).evaluateAll((images) => images.some((node) => {
    const image = node as HTMLImageElement;
    const rect = image.getBoundingClientRect();
    const style = getComputedStyle(image);
    return image.complete && image.naturalWidth > 0 && rect.width > 0 && rect.height > 0 &&
      style.display !== "none" && style.visibility !== "hidden" && Number.parseFloat(style.opacity) > 0.05;
  }));
  expect(painted, "gallery must paint at least one decoded image").toBe(true);
}

for (const viewport of breakpoints) {
  test.describe(viewport.name, () => {
    test.use({ viewport });

    test("Bollywood Actresses carousel images render and return 200", async ({ page }) => {
      const failedResponses: string[] = [];
      page.on("response", (response) => {
        if (response.url().includes("/actresses/") && response.status() !== 200) {
          failedResponses.push(`${response.status()} ${response.url()}`);
        }
      });
      const response = await page.goto("/bollywood-actress-booking/", { waitUntil: "networkidle" });
      expect(response?.status()).toBe(200);
      const selector = 'section[aria-labelledby="actress-coverflow-heading"] img[src*="/actresses/"]';
      await expect(page.locator(selector)).toHaveCount(13);
      await assertImagesDecoded(page, selector, 13);
      await assertAtLeastOnePaintedImage(page, selector);
      expect(failedResponses, failedResponses.join("\n")).toEqual([]);
    });

    test("Tamannaah gallery images render and return 200", async ({ page }) => {
      const statuses = new Map<string, number>();
      page.on("response", (response) => {
        const file = tamannaahGalleryFiles.find((name) => response.url().includes(name));
        if (file) statuses.set(file, response.status());
      });
      const response = await page.goto("/book-tamannaah-bhatia/", { waitUntil: "networkidle" });
      expect(response?.status()).toBe(200);
      for (const file of tamannaahGalleryFiles) {
        const selector = `figure img[src*="${file}"]`;
        await assertImagesDecoded(page, selector, 1);
        await page.locator(selector).first().scrollIntoViewIfNeeded();
        await assertAtLeastOnePaintedImage(page, selector);
        expect(statuses.get(file), `${file} must return HTTP 200`).toBe(200);
      }
    });
  });
}