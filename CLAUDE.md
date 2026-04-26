# CLAUDE.md - Grout Academy

> Migration from Webflow to static HTML/CSS/JS before next Webflow renewal on 2026-05-23.

## Business Context

**Business Name:** Grout Academy and Tiling
**Slogan:** Simply Smarter
**Owner:** Aaron Varley (stays anonymous - no name/title on site)
**Phone:** 0418 958 131
**Email:** groutacademy@gmail.com
**ABN:** 61 564 238 604
**Location:** Geelong & Ballarat VIC, expanding Australia-wide
**Live URL:** www.groutacademy.com.au
**Domain registrar:** Registry Australia (Aaron owns domain)

### Services
- Shower Regrouting
- Pool Regrouting
- Tile and Pavement Regrouting
- Pool Coping Tile Restoration
- Tile Repairs
- Waterproofing and Resilicone

### Service Areas (VIC)
Geelong, Melbourne, Ballarat, Colac, Apollo Bay, Teesdale, Rokewood, Lara, Bellarine, Bannockburn, Lorne, Werribee

### Social
- Facebook: Grout Academy and Tiling (Sutera Sites has partnered access)
- Google Business Profile: Active (service areas as above)

### Tracking
- Google Ads: AW-17975931257 (conversion label: `tdOOCJfahP8bEPniy_tC`, phone conversion number: 0418 958 131)
- GA4: G-K7M7GWT3RJ
- Google Site Verification: `ngd569cODajM6XLialsZIDq27v2jPc6OUpf4ffUS788`

---

## Reference Source

Current Webflow site: https://www.groutacademy.com.au/
Reference screenshots of all 12 Webflow pages in `temporary screenshots/` (named `ref-<slug>.png`).

## Site Structure (mirrors Webflow sitemap)

| Slug | File | Purpose |
|------|------|---------|
| `/` | `index.html` | Homepage |
| `/services` | `services.html` | Services overview |
| `/services/shower-regrouting-geelong` | `services/shower-regrouting-geelong.html` | Service detail |
| `/services/pool-regrouting-geelong` | `services/pool-regrouting-geelong.html` | Service detail |
| `/services/tile-and-pavement-regrouting-geelong` | `services/tile-and-pavement-regrouting-geelong.html` | Service detail |
| `/services/pool-coping-tile-restoration-geelong` | `services/pool-coping-tile-restoration-geelong.html` | Service detail |
| `/services/tile-repairs-geelong` | `services/tile-repairs-geelong.html` | Service detail |
| `/services/waterproofing-and-resilicone-geelong` | `services/waterproofing-and-resilicone-geelong.html` | Service detail |
| `/about-us` | `about-us.html` | About |
| `/contact` | `contact.html` | Contact form (Formspree) |
| `/service-areas` | `service-areas.html` | Service areas |
| `/thank-you` | `thank-you.html` | Form submission thank-you |

## Always Do First
- Invoke the `frontend-design` skill before writing any frontend code.

## Reference Matching
- Match layout, spacing, typography, and color from the Webflow reference screenshots.
- Do not redesign or add sections that aren't on the Webflow site.
- Keep copy verbatim from the scraped Webflow HTML (stored at `C:/Users/james/AppData/Local/Temp/grout_scrape/`).

## Local Server
- Start: `node serve.mjs` (serves root at `http://localhost:3000`)
- Never screenshot a `file:///` URL.

## Screenshot Workflow
- `node screenshot.mjs http://localhost:3000 <label>` saves to `temporary screenshots/screenshot-N-<label>.png`
- Reference screenshots from Webflow are prefixed `ref-`.
- Compare reference vs build, fix diffs, re-screenshot. At least 2 rounds per page.

## Output Defaults
- Single HTML file per page, all styles inline, unless told otherwise.
- Tailwind via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Google Fonts for typography (match Webflow's font stack from the shared CSS).
- Mobile-first responsive.

## Brand Assets
- `brand_assets/` contains logo variants, hero images, gallery photos - all pulled from the Webflow CDN.
- Do not use placeholders where real assets exist.

## Deployment
- Git remote: `github.com/suterasites/grout-academy` (to be created).
- Push to `main`, then Cloudflare Pages auto-deploys.
- Domain cutover (DNS via Registry Australia) happens after build review - James handles DNS.

## Multi-Page Consistency
- Navbar identical across all pages.
- Footer identical across all pages.
- Internal links use relative paths matching the sitemap structure.

## Form Handling
- Contact form on `contact.html` posts to Formspree (endpoint TBD, match the pattern used in other client sites).
- On success, redirect to `/thank-you`.

## Hard Rules
- Do not add sections, features, or content not in the Webflow reference.
- Do not "improve" the Webflow design - mirror it.
- Do not use em dashes (-) anywhere. Use hyphens, commas, or periods.
- Keep Google Ads conversion tracking and GA4 IDs intact on every page.

---

# Site Checklist

Use this checklist for every page on the site. Each page must have the metadata, schema, content, and performance items in place before being promoted (especially for paid-traffic landing pages).

## Per-Page Template

### Page: _______________

**Meta & SEO**
- [ ] Title tag - under 60 chars, includes primary keyword, brand name at end
- [ ] Meta description - under 160 chars, includes a clear CTA and primary keyword
- [ ] Canonical URL - self-referencing, matches preferred URL format (trailing slash, www)
- [ ] Open Graph title and description
- [ ] Twitter card metadata
- [ ] Geo meta tags where the page is location-targeted

**Schema & Structured Data**
- [ ] LocalBusiness or Organization identity schema
- [ ] Service schema for service detail / LP pages
- [ ] FAQPage schema where the page has an FAQ section
- [ ] BreadcrumbList for inner pages
- [ ] Validated via Google Rich Results Test, no errors

**Sitemaps & Indexing**
- [ ] Page included in XML sitemap with correct lastmod
- [ ] No `noindex` unless intentional

**Content & AI Readability**
- [ ] At least 500 words of unique body content
- [ ] Single H1, logical heading hierarchy
- [ ] Semantic HTML (section, article, p, ul) - not div soup
- [ ] All images have descriptive alt text
- [ ] Content rendered server-side (no JS-only rendering)

**Performance (PSI Mobile target: 90+)**
- [ ] CSS compiled and inlined, no Tailwind CDN at runtime
- [ ] Hero image served as responsive WebP / AVIF with `<picture>` and explicit width/height
- [ ] LCP image preloaded with `fetchpriority="high"`
- [ ] Logos sized to actual display dimensions (no 2000x2000 PNGs)
- [ ] Third-party JS (gtag, Elfsight, etc) deferred until first user interaction
- [ ] Fonts loaded with `display=swap` and non-blocking `<link rel="preload" as="style">`

---

## Page-by-Page Tracker

### Shower Regrouting Geelong (LP) - `/regrouting-geelong/`

Paid-traffic landing page for the Google Ads "Shower Regrouting Geelong" campaign. Live at https://www.groutacademy.com.au/regrouting-geelong/.

**Meta & SEO**
- [x] Title - "Shower Regrouting Geelong | Grout Academy" (44 chars)
- [x] Meta description - "Professional shower regrouting in Geelong. Mould removed, grout restored, waterproof seal protected with premium Mapei products. Free quote within 24 hours." (159 chars)
- [x] Canonical - `https://www.groutacademy.com.au/regrouting-geelong/`
- [x] Open Graph title + description + image (hero WebP)
- [x] Twitter `summary_large_image` card
- [x] Geo meta `AU-VIC` / Geelong

**Schema**
- [x] LocalBusiness, Service (Shower Regrouting), FAQPage (8 Q&A), BreadcrumbList
- [ ] Run Google Rich Results Test once after CrUX data accrues

**Sitemaps**
- [ ] Add to `sitemap.xml` once a sitemap is created for the site (no sitemap exists yet)

**Content & AI Readability**
- [x] 500+ words of unique body content
- [x] Single H1, semantic sections, descriptive alt text
- [x] Server-rendered HTML (no client-side framework)

**Performance (2026-04-26)**
- [x] PSI Mobile: 92  /  Desktop: 99
- [x] LCP 2.7s, FCP 2.7s, CLS 0.049, TBT well under 200ms after interaction-only deferral
- [x] Tailwind compiled to inline `<style>` (15 KiB) - no CDN
- [x] Hero served as 640w / 1200w WebP via `<picture>` with `fetchpriority="high"` preload
- [x] Logo resized 2000x2000 / 454 KiB to 80x80 / 2.5 KiB
- [x] gtag + Elfsight deferred until first pointerdown / touchstart / keydown / click / mousemove (no scroll trigger to avoid Lighthouse false-fire)
- [x] Cloudflare Email Obfuscation disabled in dashboard

**Tracking**
- [x] Google Ads conversion (`AW-17975931257/tdOOCJfahP8bEPniy_tC`) wired to `data-conversion="call"` phone clicks
- [x] GA4 (`G-K7M7GWT3RJ`) loaded via deferred loader
- [x] Formspree (`mojybkzj`) hidden `_source=regrouting-geelong-lp` so LP form submits are attributable

---

## Site-Wide Checks

- [ ] `sitemap.xml` created with all pages, lastmod dates, priority
- [ ] `sitemap.xml` submitted to Google Search Console
- [ ] `robots.txt` created, references sitemap, allows all crawlers
- [x] LocalBusiness identity schema on home page
- [ ] Schema validation clean across all pages (Google Rich Results Test)
- [x] Cloudflare Email Obfuscation disabled (zone-wide)

---

## Quick Reference - Character Limits

| Element | Max |
|---|---|
| Title tag | 60 |
| Meta description | 160 |
| OG title | 60 |
| OG description | 200 |
