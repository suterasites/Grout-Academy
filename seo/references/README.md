# Grout Academy Voice References

These five files are the source of truth for **how Grout Academy talks** in any new client-facing content (blog posts, service pages, city landing pages, ads, social).

**Read all five before writing a single sentence:**

1. [voice.md](./voice.md) - sentence rhythm, word choices, anti-patterns, the "tells that it's AI"
2. [humour.md](./humour.md) - **the brand does not use humour** - read this to understand why and what replaces it
3. [stats.md](./stats.md) - real numbers only; what's verified vs flagged; the things never to claim until Aaron confirms
4. [opinions.md](./opinions.md) - the small number of strong positions that separate Grout Academy from generic competitors
5. [stories.md](./stories.md) - archetypal scenarios for grounding posts (composite, not testimonials)

## How these were built

This is a **v1 draft** mined from existing material on 2026-04-30:

- Existing groutacademy.com.au site copy (homepage, six service detail pages, about, contact, /regrouting-geelong/ landing page)
- CRM client profile and notes (`CRM/clients/Grout Academy/profile.md` and `notes.md`)
- The "Simply Smarter" brand positioning Aaron originated

What was **not** available for v1:
- Direct interview with Aaron
- Recordings of Aaron explaining things in his own words
- Real customer testimonials with named permission
- Verified pricing ranges
- Verified business stats (years founded, total jobs, etc.)

## What's good in v1

- The voice rules in `voice.md` are extracted directly from the existing copy Aaron has already approved (and in places, written), so the register is consistent with what's live
- The opinions in `opinions.md` are derived from the brand's stated positions (Mapei-only, fix-it-once, no top-ups, fixed quotes) - all defensible
- The "what we never claim" section of `stats.md` locks in the lessons from the 2026-04-30 aggregate-rating cleanup (`CRM/clients/Grout Academy/notes.md`)
- The "no humour" decision in `humour.md` matches the brand's anonymous-owner positioning - personality humour requires a personality

## What needs Aaron's input to upgrade to v2

(Listed in priority order - i.e. what would most improve the content quality.)

1. **Year founded / years in operation** - to back any "since X" or "X+ years" claim
2. **Pricing ranges** - so service pages can publish bands ("most jobs $X to $Y") instead of qualitative pricing language. This is the single biggest CRO unlock.
3. **Three to five real recent jobs** with customer permission to mention suburb + outcome - replaces archetypes in `stories.md`
4. **Total jobs done / showers regrouted** - if a number is genuinely available, it can be claimed
5. **Why Aaron started Grout Academy** - the origin story, even kept anonymous, would give us one foundational anecdote to anchor an "About" rewrite around
6. **The job that made him decide cheap product was unacceptable** - the moment that committed the business to Mapei-only. This is the heart of the brand and would land hard if it's a real story

If Aaron will sit for a 30-minute call (or even a voice note answering the above six questions), v2 of these files would be substantially stronger.

## Where these files live and how they're used

- These files are not deployed to the live site. They are working docs for content generation.
- New blog posts and service pages should reference these files via the SEO Phase 4 workflow (`CRM/operations/sops/seo-optimisation.md`).
- If the brand voice ever needs to be expressed elsewhere (a new ad campaign, a social caption series, a capability statement), pull from these files first instead of inventing new copy.

## Update cadence

- Update whenever Aaron clarifies something verifiable (pricing, real story, a new strong opinion).
- Re-check the "things to avoid claiming" list in `stats.md` against the live site quarterly to catch any drift.
- If the brand fundamentally repositions (Aaron going on-camera, expanding interstate, launching a different sub-brand), revisit the whole set.
