# Developer App Website Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bilingual, SEO-focused developer website that showcases four apps and drives visitors to App Store downloads.

**Architecture:** Use a small static site with one shared stylesheet and separate HTML pages for the home page, each app, and each SEO article. Keep metadata server-rendered in the HTML so search crawlers see complete titles, descriptions, and structured data without client-side dependence.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, XML sitemap, robots.txt

---

## Chunk 1: Site foundation and shared styling

### Task 1: Create the site shell

**Files:**
- Create: `index.html`
- Create: `assets/css/site.css`
- Create: `assets/js/site.js`
- Create: `robots.txt`
- Create: `sitemap.xml`

- [ ] **Step 1: Write the home page markup**

Create a bilingual home page with:
- hero section
- four app cards
- trust/value section
- FAQ section
- App Store CTAs in hero, cards, and footer
- full `<head>` metadata: `<title>`, meta description, canonical URL, Open Graph tags, `hreflang` links for Chinese and English

- [ ] **Step 2: Write the shared stylesheet**

Define layout, spacing, typography, card styles, CTA buttons, responsive grid, and light/dark-safe colors.

- [ ] **Step 3: Add minimal shared JavaScript**

Implement only small usability helpers if needed, such as smooth scrolling or language toggle support. Keep all content in HTML for SEO.

- [ ] **Step 4: Add crawler-facing files**

Create `robots.txt` that allows indexing and points to `sitemap.xml`. Create `sitemap.xml` with the home page, app pages, and article pages.

- [ ] **Step 5: Validate locally**

Run:

```bash
python3 -m http.server 8080
```

Expected: site serves at `http://localhost:8080/` and returns `200` for `index.html`, `robots.txt`, and `sitemap.xml`.

- [ ] **Step 6: Verify SEO head output**

Run:

```bash
curl -s http://localhost:8080/ | grep -E '<title>|<meta name="description"|canonical|hreflang'
```

Expected: all four patterns match.

---

## Chunk 2: App detail pages and SEO content

### Task 2: Create app landing pages

**Files:**
- Create: `apps/noteit.html`
- Create: `apps/rss-reader.html`
- Create: `apps/mahjong-ai.html`
- Create: `apps/fitpretty.html`

- [ ] **Step 1: Write each app page**

For each app page write primary copy in Chinese and add English parallel text for the headline, summary, and CTA. Include:
- unique `<title>` and meta description
- canonical URL
- Open Graph tags
- `hreflang` links for Chinese and English versions
- `SoftwareApplication` structured data
- screenshot or gallery section
- feature bullets
- use-case section
- FAQ section
- App Store download button

- [ ] **Step 2: Add internal links**

Link each app page back to the home page and forward to related article pages.

- [ ] **Step 3: Validate metadata**

Confirm each page has unique title/description text and no duplicate canonical URLs.

- [ ] **Step 4: Validate page delivery**

Run:

```bash
curl -I http://localhost:8080/apps/noteit.html
```

Expected: `HTTP/1.0 200 OK` or equivalent success response.

### Task 3: Create SEO article pages

**Files:**
- Create: `articles/ai-journal-app-for-reflection.html`
- Create: `articles/rss-reader-for-information-overload.html`
- Create: `articles/mahjong-assistant-practice-guide.html`
- Create: `articles/fitness-app-for-body-transformation.html`

- [ ] **Step 1: Write search-intent articles**

Each article should answer a specific query, explain the problem, and recommend the matching app. Write the main copy in Chinese and include English parallel text for the headline, summary, and CTA blocks.

- [ ] **Step 2: Add conversion blocks**

Include in-article download CTA blocks, related app cards, and FAQ schema where appropriate.

- [ ] **Step 3: Add article SEO metadata**

For each article include:
- unique `<title>` and meta description
- canonical URL
- Open Graph tags
- `hreflang` links for Chinese and English versions

- [ ] **Step 4: Update sitemap**

Add all article URLs to `sitemap.xml`.

- [ ] **Step 5: Validate crawlability**

Run:

```bash
curl -I http://localhost:8080/articles/ai-journal-app-for-reflection.html
```

Expected: `HTTP/1.0 200 OK` or equivalent success response.

---

## Chunk 3: Polish, consistency, and final verification

### Task 4: Tighten copy and cross-linking

**Files:**
- Modify: `index.html`
- Modify: `apps/*.html`
- Modify: `articles/*.html`
- Modify: `assets/css/site.css`

- [ ] **Step 1: Ensure bilingual consistency**

Check that the hero headline, app summaries, CTA labels, and article intros are bilingual where they matter most and that Chinese remains primary.

- [ ] **Step 2: Strengthen download funnel**

Ensure every page has at least one visible App Store CTA above the fold and one near the end.

- [ ] **Step 3: Improve internal linking**

Each article should point to the relevant app page; each app page should point to related articles.

- [ ] **Step 4: Final local review**

Open the homepage and representative app/article pages in a browser and confirm mobile layout, readability, and CTA prominence.

- [ ] **Step 5: Mark complete**

Update the session todo status to done for the site build and keep the site ready for deployment.
