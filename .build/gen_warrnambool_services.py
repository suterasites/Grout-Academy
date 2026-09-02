#!/usr/bin/env python3
"""
Generate the 6 Warrnambool service pages by cloning the canonical Geelong
service pages and surgically localising them to Warrnambool / SW-coast Victoria.

Deterministic + idempotent: nav, footer, <script> blocks, GA/gtag tags,
SUTERA_LEAD_EVENTS, styles and images are preserved byte-for-byte (they are
never targeted). Only the head SEO block, schema areaServed, breadcrumb, H1,
hero, intro, cross-sell cluster, recent-work heading, and FAQ are changed.

Run from anywhere:  python3 .build/gen_warrnambool_services.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SERVICES = os.path.normpath(os.path.join(HERE, "..", "services"))

SLUGS = [
    "shower-regrouting",
    "pool-regrouting",
    "tile-and-pavement-regrouting",
    "pool-coping-tile-restoration",
    "tile-repairs",
    "waterproofing-and-resilicone",
]

# Genuine local angle: Warrnambool + Port Fairy + Portland are coastal SW Victoria.
COASTAL_P = (
    '<p class="text-ink-soft text-lg">Warrnambool sits right on the coast, and salt '
    'air and high humidity work against grout and silicone every day. Sealed joints '
    'break down faster on the South-West coast than they do inland, so staying on top '
    'of regrouting and resiliconing keeps water where it belongs and protects your '
    'tiles. We cover Warrnambool, Port Fairy, Portland, Koroit, Camperdown and Terang.</p>'
)

LOCAL_FAQ_JSON = (
    '{ "@type": "Question", "name": "Do you service Warrnambool and the surrounding '
    'South-West towns?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. We cover '
    'Warrnambool, Port Fairy, Portland, Koroit, Camperdown, Terang and the wider '
    'South-West. Coastal salt air breaks grout and silicone down faster here, so regular '
    'regrouting and resiliconing matters more on the coast. Contact us for a free quote '
    'anywhere in the region." }},'
)

LOCAL_FAQ_HTML = (
    '<details class="faq-item border border-ink-line rounded-lg p-5"><summary '
    'class="flex items-center justify-between font-semibold text-lg">Do you service '
    'Warrnambool and the surrounding South-West towns?<svg class="faq-chevron w-5 h-5" '
    'viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 '
    '0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 '
    '0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd"/></svg></summary><p '
    'class="mt-4 text-ink-soft">Yes. We cover Warrnambool, Port Fairy, Portland, Koroit, '
    'Camperdown, Terang and the wider South-West. Coastal salt air breaks grout and '
    'silicone down faster here, so regular regrouting and resiliconing matters more on '
    'the coast. Contact us for a free quote anywhere in the region.</p></details>'
)


def transform(html: str) -> str:
    # 1. Prose region phrases (both head descriptions and body hero subtext).
    html = html.replace("Geelong, Melbourne and Ballarat", "Warrnambool, Port Fairy and Portland")
    html = html.replace(
        "Geelong, Melbourne, Ballarat and surrounding regions",
        "Warrnambool, Port Fairy, Portland and the wider South-West",
    )

    # Split head / body so blanket "Geelong" swaps never touch the footer boilerplate.
    b = html.index("<body")
    head, body = html[:b], html[b:]

    # 2. HEAD: schema areaServed -> SW-coast region (Melbourne/Ballarat now only in schema).
    head = head.replace('"name": "Melbourne"', '"name": "Port Fairy"')
    head = head.replace('"name": "Ballarat"', '"name": "Portland"')
    head = head.replace('"name": "Bellarine Peninsula"', '"name": "Koroit"')
    head = head.replace('"name": "Surf Coast"', '"name": "South-West Victoria"')
    # 3. HEAD: self-referential URL slugs + remaining display "Geelong".
    # Both URL forms, because the sitemap and every canonical moved to clean URLs on
    # 2026-09-02 (Cloudflare 308s .html -> extensionless, so declaring .html handed
    # Google a URL that bounces). Matching only the .html form here would leave a
    # regenerated page declaring the GEELONG canonical - a brand new page announcing
    # itself as a duplicate of the one it was cloned from. The trailing quote keeps
    # this to URL ends, so prose mentioning Geelong is untouched.
    head = head.replace("-geelong.html", "-warrnambool.html")
    head = head.replace('-geelong"', '-warrnambool"')
    head = head.replace("Geelong", "Warrnambool")

    # Split body at the footer; everything after stays identical to the rest of the site.
    f = body.index("<!-- FOOTER -->")
    pre, foot = body[:f], body[f:]

    # 4. PRE-FOOTER: cross-sell cards only (card <a> uniquely carries the "block bg-white
    #    border" class); nav/mobile/footer service links do not match this pattern.
    pre = pre.replace(
        '-geelong.html" class="block bg-white border',
        '-warrnambool.html" class="block bg-white border',
    )
    # 5. PRE-FOOTER: breadcrumb, H1, hero, intro, section headings.
    pre = pre.replace("Geelong", "Warrnambool")
    pre = pre.replace(
        "Finished Jobs Across Warrnambool",
        "Finished Jobs Across Warrnambool and the South-West",
    )

    html = head + pre + foot

    # 6. Inject the coastal paragraph right after the intro paragraph (unique mb-4 class).
    html = re.sub(
        r'(<p class="text-ink-soft text-lg mb-4">.*?</p>)',
        lambda m: m.group(1) + "\n        " + COASTAL_P,
        html, count=1, flags=re.S,
    )
    # 7. Inject the local FAQ first, in both the schema graph and the visible list.
    html = html.replace('"mainEntity": [\n          ', '"mainEntity": [\n          ' + LOCAL_FAQ_JSON + '\n          ', 1)
    html = html.replace('<details class="faq-item', LOCAL_FAQ_HTML + '\n        <details class="faq-item', 1)
    return html


def main():
    for slug in SLUGS:
        src = os.path.join(SERVICES, f"{slug}-geelong.html")
        dst = os.path.join(SERVICES, f"{slug}-warrnambool.html")
        with open(src, encoding="utf-8") as fh:
            html = fh.read()
        out = transform(html)
        # Guards: fail loudly if anything is off.
        assert "-geelong.html" not in out.split("<!-- FOOTER -->")[0].split("<body")[0], f"{slug}: geelong slug left in head"
        assert "Geelong" not in out.split("<!-- FOOTER -->")[0], f"{slug}: 'Geelong' left in head/pre-footer"
        assert "Warrnambool" in out, f"{slug}: no Warrnambool text"
        assert out.count("SUTERA_LEAD_EVENTS") == 1, f"{slug}: lead-events snippet altered"
        assert "AW-17960926932" in out and "G-K7M7GWT3RJ" in out, f"{slug}: tracking IDs dropped"
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"  wrote {os.path.relpath(dst, os.path.join(HERE, '..'))}  ({len(out)} bytes)")


if __name__ == "__main__":
    main()
