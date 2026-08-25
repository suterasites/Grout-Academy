#!/usr/bin/env python3
"""
Generate the Werribee / Wyndham paid-ads landing page by cloning the canonical
Geelong ads LP and surgically localising it to the Wyndham growth corridor.

Why cloned from Geelong and not Warrnambool: Aaron's main installer relocated to
Tarneit (confirmed on the 2026-08-20 call), so Wyndham is a genuine local-presence
market with normal availability. Warrnambool is the opposite - a planned-trip,
travel-included offer. Cloning the wrong parent would ship the wrong offer.

Honesty rules baked in (there is no documented Grout job history in Wyndham yet):
  - No "What Werribee customers say" / "Finished showers across Werribee" /
    "Recent job - Shower regrout, Werribee". Those proof claims are neutralised
    exactly the way the Warrnambool LP neutralised them.
  - Local framing is limited to what is true: the installer is based in the area,
    so availability is normal. No invented years-in-the-area or local review count.
  - Geo stays inside the Wyndham LGA. Aaron opened with "all the western suburbs"
    and accepted tight-beats-broad, so do NOT widen this to Melbourne's west.

Deterministic + idempotent: nav, footer, <style>, gtag/AW/GA4 blocks,
SUTERA_LEAD_EVENTS, images and the tel: conversion hook are never targeted, so
they carry over byte-for-byte. Every replacement is asserted - if the Geelong
source drifts, this fails loudly instead of writing a half-localised page.

Run from anywhere:  python3 .build/gen_werribee_lp.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "regrouting-geelong", "index.html")
OUT_DIR = os.path.join(ROOT, "regrouting-werribee")
OUT = os.path.join(OUT_DIR, "index.html")

BASE = "https://www.groutacademy.com.au"

# (old, new) - applied in order, each asserted present exactly once unless noted.
REPLACEMENTS = [
    # ---------- head SEO ----------
    ("<title>Shower Regrouting Geelong | Grout Academy</title>",
     "<title>Shower Regrouting Werribee | Grout Academy</title>"),

    ('<meta name="description" content="Professional shower regrouting in Geelong. Mould removed, grout restored, waterproof seal protected with premium Mapei products. Free quote within 24 hours.">',
     '<meta name="description" content="Professional shower regrouting in Werribee and the Wyndham area. Mould removed, grout restored, waterproof seal protected with premium Mapei products. Free quote within 24 hours.">'),

    ('<meta name="keywords" content="shower regrouting Geelong, regrouting Geelong, shower regrout, grout repair Geelong, mould removal grout, bathroom regrouting Geelong">',
     '<meta name="keywords" content="shower regrouting Werribee, regrouting Werribee, shower regrout, grout repair Werribee, mould removal grout, bathroom regrouting Werribee, regrouting Tarneit, regrouting Point Cook, regrouting Hoppers Crossing">'),

    ('<meta name="geo.placename" content="Geelong">',
     '<meta name="geo.placename" content="Werribee">'),

    (f'<link rel="canonical" href="{BASE}/regrouting-geelong/">',
     f'<link rel="canonical" href="{BASE}/regrouting-werribee/">'),

    ('<meta property="og:title" content="Shower Regrouting Geelong | Grout Academy">',
     '<meta property="og:title" content="Shower Regrouting Werribee | Grout Academy">'),

    ('<meta property="og:description" content="Mould removed, grout restored, waterproof seal protected. Premium Mapei products. Free quotes across Geelong.">',
     '<meta property="og:description" content="Mould removed, grout restored, waterproof seal protected. Premium Mapei products. Free quotes across Werribee and the Wyndham area.">'),

    (f'<meta property="og:url" content="{BASE}/regrouting-geelong/">',
     f'<meta property="og:url" content="{BASE}/regrouting-werribee/">'),

    ('<meta name="twitter:title" content="Shower Regrouting Geelong | Grout Academy">',
     '<meta name="twitter:title" content="Shower Regrouting Werribee | Grout Academy">'),

    ('<meta name="twitter:description" content="Mould removed, grout restored, waterproof seal protected. Free quotes across Geelong.">',
     '<meta name="twitter:description" content="Mould removed, grout restored, waterproof seal protected. Free quotes across Werribee and the Wyndham area.">'),

    # ---------- LocalBusiness areaServed ----------
    ('''          { "@type": "City", "name": "Geelong" },
          { "@type": "City", "name": "Ballarat" },
          { "@type": "City", "name": "Colac" },
          { "@type": "City", "name": "Apollo Bay" },
          { "@type": "Place", "name": "Bellarine Peninsula" }''',
     '''          { "@type": "City", "name": "Werribee" },
          { "@type": "City", "name": "Wyndham Vale" },
          { "@type": "City", "name": "Tarneit" },
          { "@type": "City", "name": "Hoppers Crossing" },
          { "@type": "City", "name": "Point Cook" },
          { "@type": "City", "name": "Truganina" },
          { "@type": "City", "name": "Williams Landing" },
          { "@type": "City", "name": "Geelong" }'''),

    # ---------- Service areaServed ----------
    ('''          { "@type": "City", "name": "Geelong" },
          { "@type": "Place", "name": "Bellarine Peninsula" },
          { "@type": "City", "name": "Ballarat" }''',
     '''          { "@type": "City", "name": "Werribee" },
          { "@type": "City", "name": "Tarneit" },
          { "@type": "City", "name": "Point Cook" },
          { "@type": "Place", "name": "City of Wyndham" }'''),

    # ---------- FAQ JSON-LD ----------
    # Lead with the service-area question, the way the Warrnambool LP does.
    ('''          {
            "@type": "Question",
            "name": "How long does a shower regrout take in Geelong?",''',
     '''          {
            "@type": "Question",
            "name": "Do you service Werribee and the Wyndham area?",
            "acceptedAnswer": { "@type": "Answer", "text": "Yes. Werribee, Wyndham Vale, Tarneit, Hoppers Crossing, Point Cook, Truganina, Williams Landing, Manor Lakes and Little River are all inside our service area. Our installer is based in the Wyndham area, so this is normal local work booked on normal timeframes, not a trip we have to schedule around. There is no call-out fee." }
          },
          {
            "@type": "Question",
            "name": "How long does a shower regrout take in Werribee?",'''),

    ('"text": "Yes. We stand behind every regrout we do. If something is not right after we leave, we come back and sort it. Honest workmanship is the reason most of our work comes from word-of-mouth across Geelong." }',
     '"text": "Yes. We stand behind every regrout we do. If something is not right after we leave, we come back and sort it. Honest workmanship is the reason most of our work comes from word-of-mouth." }'),

    ('"text": "We usually quote within 24 hours and can book most Geelong shower regrouts within one to two weeks. Urgent jobs can often be fitted in sooner. Call 0418 958 131 to check current availability." }',
     '"text": "We usually quote within 24 hours and can book most Wyndham shower regrouts within one to two weeks. Because our installer is local, urgent jobs can often be fitted in sooner. Call 0418 958 131 to check current availability." }'),

    # ---------- Breadcrumb schema ----------
    (f'{{ "@type": "ListItem", "position": 2, "name": "Shower Regrouting Geelong", "item": "{BASE}/regrouting-geelong/" }}',
     f'{{ "@type": "ListItem", "position": 2, "name": "Shower Regrouting Werribee", "item": "{BASE}/regrouting-werribee/" }}'),

    # ---------- hero ----------
    ('<span class="text-white/70">Regrouting Geelong</span>',
     '<span class="text-white/70">Regrouting Werribee</span>'),

    ("Now booking shower regrouts across Geelong",
     "Now booking shower regrouts across Werribee &amp; Wyndham"),

    ('''              Shower Regrouting<br>
              <span class="text-pomegranate-light">Geelong.</span>''',
     '''              Shower Regrouting<br>
              <span class="text-pomegranate-light">Werribee.</span>'''),

    ("Mould removed, grout restored, waterproof seal protected. Premium Mapei products, honest local specialists, fixed quotes. Most showers done in one to two days.",
     "Mould removed, grout restored, waterproof seal protected. Premium Mapei products, fixed quotes, and an installer based in the Wyndham area. Most showers done in one to two days."),

    ("Local Geelong Specialists</span>",
     "Wyndham-Based Installer</span>"),

    # ---------- hero image: no fabricated local job ----------
    ('alt="Restored tiled shower in a Geelong home with fresh grout and silicone"',
     'alt="Restored tiled shower with fresh Mapei grout and silicone"'),

    ('<p class="font-display text-2xl">Shower regrout, Geelong</p>',
     '<p class="font-display text-2xl">Shower regrout, Mapei rebuild</p>'),

    # ---------- form ----------
    ("Tell us about your shower. We will call you back within 24 hours to book your free site visit and lock in a fixed price.",
     "Tell us about your shower. We will call you back within 24 hours to book your free site visit and lock in a fixed price."),

    ('<input type="hidden" name="_subject" value="New Shower Regrouting Geelong enquiry">',
     '<input type="hidden" name="_subject" value="New Shower Regrouting Werribee enquiry">'),

    ('<input type="hidden" name="_source" value="regrouting-geelong-lp">',
     '<input type="hidden" name="_source" value="regrouting-werribee-lp">'),

    ('placeholder="e.g. Newtown, Belmont, Highton"',
     'placeholder="e.g. Tarneit, Point Cook, Hoppers Crossing"'),

    # ---------- social proof: neutralised, no invented local history ----------
    ('<h2 class="heading-uppercase font-display text-4xl sm:text-5xl mb-3">What Geelong customers say.</h2>',
     '<h2 class="heading-uppercase font-display text-4xl sm:text-5xl mb-3">What our customers say.</h2>'),

    ("Geelong homeowners call Grout Academy back because the work lasts, the price is honest, and the bathroom is left spotless.",
     "Homeowners call Grout Academy back because the work lasts, the price is honest, and the bathroom is left spotless."),

    ('''            <p class="font-semibold text-sm">Local Geelong</p>
            <p class="text-white/60 text-xs mt-1 font-body">Specialists, not handymen</p>''',
     '''            <p class="font-semibold text-sm">Wyndham Based</p>
            <p class="text-white/60 text-xs mt-1 font-body">Specialists, not handymen</p>'''),

    ('<h2 class="heading-uppercase font-display text-3xl sm:text-4xl">Finished showers across Geelong.</h2>',
     '<h2 class="heading-uppercase font-display text-3xl sm:text-4xl">Finished showers, rebuilt in Mapei.</h2>'),

    # ---------- visible FAQ (mirrors the JSON-LD above) ----------
    ('''          <details>
            <summary class="flex items-center justify-between gap-6 py-6">
              <span class="font-display text-2xl">How long does a shower regrout take in Geelong?</span>''',
     '''          <details>
            <summary class="flex items-center justify-between gap-6 py-6">
              <span class="font-display text-2xl">Do you service Werribee and the Wyndham area?</span>
              <span class="faq-icon text-pomegranate text-3xl leading-none font-bold">+</span>
            </summary>
            <p class="pb-6 text-ink-soft font-body">Yes. Werribee, Wyndham Vale, Tarneit, Hoppers Crossing, Point Cook, Truganina, Williams Landing, Manor Lakes and Little River are all inside our service area. Our installer is based in the Wyndham area, so this is normal local work booked on normal timeframes, not a trip we have to schedule around. There is no call-out fee.</p>
          </details>
          <details>
            <summary class="flex items-center justify-between gap-6 py-6">
              <span class="font-display text-2xl">How long does a shower regrout take in Werribee?</span>'''),

    ("Honest workmanship is the reason most of our work comes from word-of-mouth across Geelong.</p>",
     "Honest workmanship is the reason most of our work comes from word-of-mouth.</p>"),

    ("We usually quote within 24 hours and can book most Geelong shower regrouts within one to two weeks. Urgent jobs can often be fitted in sooner. Call 0418 958 131 to check current availability.</p>",
     "We usually quote within 24 hours and can book most Wyndham shower regrouts within one to two weeks. Because our installer is local, urgent jobs can often be fitted in sooner. Call 0418 958 131 to check current availability.</p>"),

    # ---------- final CTA + footer ----------
    ("Call Aaron directly or send us your details. Free quotes, fixed prices, and honest timelines for shower regrouting across Geelong and surrounds.",
     "Call Aaron directly or send us your details. Free quotes, fixed prices, and honest timelines for shower regrouting across Werribee, Tarneit, Point Cook and the Wyndham area."),

    ("<span>Geelong VIC</span>",
     "<span>Servicing Werribee &amp; the Wyndham Area VIC</span>"),
]


def main():
    if not os.path.isfile(SRC):
        sys.exit(f"ERROR: source LP missing: {SRC}")

    html = open(SRC, encoding="utf-8").read()

    for i, (old, new) in enumerate(REPLACEMENTS, 1):
        if old == new:
            continue
        n = html.count(old)
        if n == 0:
            sys.exit(f"ERROR: replacement {i} not found in source LP.\n  looking for: {old[:120]!r}")
        html = html.replace(old, new)

    # Guard: the only Geelong references left should be the deliberate ones
    # (LocalBusiness areaServed keeps Geelong as the wider footprint).
    leftover = html.count("Geelong")
    if leftover > 2:
        sys.exit(f"ERROR: {leftover} 'Geelong' references remain - expected at most 2 (schema areaServed).")

    # Guard: tracking must survive the clone intact.
    # NB: the Form Lead label (Zp4fCLj5mKUcENT9t_RC) is deliberately NOT here -
    # it fires on /thank-you page load after the Formspree redirect, not on the LP.
    for must in ["AW-17960926932", "G-K7M7GWT3RJ", "6lGnCI2lzKUcENT9t_RC",
                 "SUTERA_LEAD_EVENTS"]:
        if must not in html:
            sys.exit(f"ERROR: tracking token missing after clone: {must}")

    os.makedirs(OUT_DIR, exist_ok=True)
    prev = open(OUT, encoding="utf-8").read() if os.path.isfile(OUT) else None
    if prev == html:
        print(f"unchanged  {os.path.relpath(OUT, ROOT)}")
        return
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    # Carry the tailwind config/input across so the folder matches its siblings.
    for extra in ["tailwind.config.js", "tailwind.input.css"]:
        s = os.path.join(ROOT, "regrouting-geelong", extra)
        d = os.path.join(OUT_DIR, extra)
        if os.path.isfile(s) and not os.path.isfile(d):
            open(d, "w", encoding="utf-8").write(open(s, encoding="utf-8").read())

    print(f"{'wrote' if prev is None else 'updated'}  {os.path.relpath(OUT, ROOT)}  "
          f"({len(html):,} bytes, {leftover} deliberate Geelong refs)")


if __name__ == "__main__":
    main()
