import { expect, test } from "@playwright/test";

// Slugs from the actress roster (see assets/bollywood-actress-booking-*.js).
// Ordered as rendered in the DOM — Deepika is the LCP candidate and MUST stay eager.
const ROSTER = [
  "deepika-padukone",
  "alia-bhatt",
  "priyanka-chopra",
  "katrina-kaif",
  "anushka-sharma",
  "kareena-kapoor",
  "kiara-adwani",
  "rashmika-mandanna",
  "tamanna-bhatia",
  "janhvi-kapoor",
  "sara-ali-khan",
  "nora-fatehi",
  "disha-patani",
];

test.describe("bollywood-actress-booking gallery SEO", () => {
  test.use({ viewport: { width: 1280, height: 900 } });

  test("every roster image has descriptive alt text and correct loading attrs", async ({ page }) => {
    await page.goto("/bollywood-actress-booking/", { waitUntil: "domcontentloaded" });
    const selector = 'section[aria-labelledby="actress-coverflow-heading"] img[src*="/actresses/"]';
    await page.waitForSelector(selector);

    // The SEO enhancer runs post-hydration via setInterval + MutationObserver.
    // Poll until every image has been stamped with data-tkc-seo="1".
    await expect
      .poll(
        () =>
          page.locator(selector).evaluateAll((imgs) =>
            imgs.filter((el) => (el as HTMLImageElement).dataset.tkcSeo === "1").length,
          ),
        { timeout: 15_000 },
      )
      .toBe(ROSTER.length);

    const data = await page.locator(selector).evaluateAll((imgs) =>
      imgs.map((el) => {
        const img = el as HTMLImageElement;
        return {
          src: img.getAttribute("src") || "",
          alt: img.getAttribute("alt") || "",
          loading: img.getAttribute("loading") || "",
          fetchpriority: img.getAttribute("fetchpriority") || "",
          decoding: img.getAttribute("decoding") || "",
        };
      }),
    );

    expect(data).toHaveLength(ROSTER.length);

    for (const item of data) {
      const alt = item.alt.toLowerCase();
      // Alt text: descriptive, not just the filename or the bare name.
      expect(item.alt.length, `alt too short for ${item.src}`).toBeGreaterThanOrEqual(60);
      expect(alt, `alt missing TKC Talent attribution for ${item.src}`).toContain("tkc talent");
      expect(alt, `alt missing booking context for ${item.src}`).toMatch(/book|booking|hire/);
      expect(alt, `alt missing event context for ${item.src}`).toMatch(/bollywood|event|brand|wedding/);
      // Async decoding on every image.
      expect(item.decoding).toBe("async");
    }

    // Deepika (first-in-DOM slug) is the LCP candidate.
    const lcp = data.find((d) => d.src.includes("deepika-padukone"));
    expect(lcp, "Deepika roster image must be present").toBeTruthy();
    expect(lcp!.loading).toBe("eager");
    expect(lcp!.fetchpriority).toBe("high");

    // Every other image must be lazy + low priority.
    for (const item of data) {
      if (item.src.includes("deepika-padukone")) continue;
      expect(item.loading, `${item.src} must be loading=lazy`).toBe("lazy");
      expect(item.fetchpriority, `${item.src} must be fetchpriority=low`).toBe("low");
    }
  });
});