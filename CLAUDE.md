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
- Google Ads: AW-17960926932 (active account, switched 2026-05-01 from dead AW-17975931257)
  - Form Lead conversion label: `Zp4fCLj5mKUcENT9t_RC` (fires on /thank-you page load post Formspree redirect)
  - Phone Call Lead conversion label: `6lGnCI2lzKUcENT9t_RC` (fires on tel: link click on regrouting-geelong LP)
  - Enhanced Conversions for Leads enabled on both, data source = "API or upload"
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
