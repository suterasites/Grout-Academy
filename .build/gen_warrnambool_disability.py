#!/usr/bin/env python3
"""
Generate the Warrnambool Disability Access Rails page by cloning the canonical
Geelong page and surgically localising it to Warrnambool / SW-coast Victoria.
Completes the Warrnambool cluster to 7/7 (matches Geelong) per Aaron's
2026-08-04 request to lead with Geelong + Warrnambool.

Companion to gen_warrnambool_services.py, but the local angle here is aged-care /
regional access (older population, spread-out towns), NOT the salt-air/grout angle
used for the regrouting pages.

Deterministic + idempotent: nav, footer, <script> blocks, GA/gtag tags,
SUTERA_LEAD_EVENTS, styles and images are preserved byte-for-byte. Only the head
SEO block, schema areaServed, breadcrumb, H1, hero, intro, cross-sell cluster and
FAQ are changed.

Run from anywhere:  python3 .build/gen_warrnambool_disability.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SERVICES = os.path.normpath(os.path.join(HERE, "..", "services"))
SLUG = "disability-access-rails"

# Local angle: SW-coast is older + spread out, and access rails are the service.
LOCAL_ANGLE_P = (
    '<p class="text-ink-soft text-lg">Warrnambool and the South-West have a large '
    'older population and towns spread out along the coast, where waiting on a '
    'tradesperson to drive down from the city can take weeks. We install grab rails, '
    'hand rails, shower rails and ambulant rails across Warrnambool, Port Fairy, '
    'Portland, Koroit, Camperdown and Terang, fixed back to solid structure and '
    'sealed so your waterproofing stays intact.</p>'
)

LOCAL_FAQ_JSON = (
    '{ "@type": "Question", "name": "Do you install access rails in Warrnambool and '
    'the surrounding South-West towns?", "acceptedAnswer": { "@type": "Answer", "text": '
    '"Yes. We install grab rails, hand rails, shower rails and ambulant rails across '
    'Warrnambool, Port Fairy, Portland, Koroit, Camperdown, Terang and the wider '
    'South-West. Every rail is fixed back to solid structure and sealed to keep your '
    'waterproofing intact. Contact us for a free quote anywhere in the region." }},'
)

LOCAL_FAQ_HTML = (
    '<details class="faq-item border border-ink-line rounded-lg p-5"><summary '
    'class="flex items-center justify-between font-semibold text-lg">Do you install '
    'access rails in Warrnambool and the surrounding South-West towns?<svg '
    'class="faq-chevron w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path '
    'fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 '
    '111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" '
    'clip-rule="evenodd"/></svg></summary><p class="mt-4 text-ink-soft">Yes. We install '
    'grab rails, hand rails, shower rails and ambulant rails across Warrnambool, Port '
    'Fairy, Portland, Koroit, Camperdown, Terang and the wider South-West. Every rail is '
    'fixed back to solid structure and sealed to keep your waterproofing intact. Contact '
    'us for a free quote anywhere in the region.</p></details>'
)


def transform(html: str) -> str:
    b = html.index("<body")
    head, body = html[:b], html[b:]

    # HEAD: schema areaServed -> SW-coast region (Melbourne/Ballarat only lived in schema).
    head = head.replace('"name": "Melbourne"', '"name": "Port Fairy"')
    head = head.replace('"name": "Ballarat"', '"name": "Portland"')
    head = head.replace('"name": "Bellarine Peninsula"', '"name": "Koroit"')
    head = head.replace('"name": "Surf Coast"', '"name": "South-West Victoria"')
    # HEAD: self-referential slugs, then any remaining display "Geelong".
    head = head.replace("-geelong.html", "-warrnambool.html")
    head = head.replace("Geelong", "Warrnambool")

    # Body split at footer; footer stays identical to the rest of the site.
    f = body.index("<!-- FOOTER -->")
    pre, foot = body[:f], body[f:]

    # PRE-FOOTER: collapse the post-2026-08-04 "Geelong, Warrnambool, Ballarat" triplet
    # BEFORE the blanket swap, otherwise it becomes "Warrnambool, Warrnambool, Ballarat".
    pre = pre.replace(
        "Geelong, Warrnambool, Ballarat and surrounding regions",
        "Warrnambool, Port Fairy, Portland and the wider South-West",
    )
    pre = pre.replace(
        "Geelong, Warrnambool and Ballarat",
        "Warrnambool, Port Fairy and Portland",
    )
    # Cross-sell cards -> Warrnambool service pages (unique "block bg-white border" class;
    # nav/mobile/footer service links stay lowercase -geelong.html, matching every page).
    pre = pre.replace(
        '-geelong.html" class="block bg-white border',
        '-warrnambool.html" class="block bg-white border',
    )
    # Remaining display "Geelong" -> Warrnambool (breadcrumb, H1, cross-sell heading).
    pre = pre.replace("Geelong", "Warrnambool")

    html = head + pre + foot

    # Inject the local angle paragraph after the intro paragraph (unique mb-4 class).
    html = re.sub(
        r'(<p class="text-ink-soft text-lg mb-4">.*?</p>)',
        lambda m: m.group(1) + "\n        " + LOCAL_ANGLE_P,
        html, count=1, flags=re.S,
    )
    # Inject the local FAQ first, in both the schema graph and the visible list.
    html = re.sub(
        r'("mainEntity":\s*\[\s*)',
        lambda m: m.group(1) + LOCAL_FAQ_JSON + "\n          ",
        html, count=1,
    )
    html = html.replace('<details class="faq-item', LOCAL_FAQ_HTML + '\n        <details class="faq-item', 1)
    return html


def main():
    src = os.path.join(SERVICES, f"{SLUG}-geelong.html")
    dst = os.path.join(SERVICES, f"{SLUG}-warrnambool.html")
    with open(src, encoding="utf-8") as fh:
        html = fh.read()
    src_foot = html.split("<!-- FOOTER -->", 1)[1]
    out = transform(html)
    # Guards: fail loudly if anything is off.
    head_pre = out.split("<!-- FOOTER -->")[0]
    assert "-geelong.html" not in head_pre.split("<body")[0], "geelong slug left in head"
    assert "Geelong" not in head_pre, "'Geelong' left in head/pre-footer"
    assert "Warrnambool, Warrnambool" not in out, "region triplet doubled up"
    assert "Warrnambool" in out, "no Warrnambool text"
    assert out.split("<!-- FOOTER -->", 1)[1] == src_foot, "footer not byte-identical"
    assert out.count("SUTERA_LEAD_EVENTS") == 1, "lead-events snippet altered"
    assert "AW-17960926932" in out and "G-K7M7GWT3RJ" in out, "tracking IDs dropped"
    assert out.count("mainEntity") == 1 and out.count('"@type": "FAQPage"') == 1, "FAQ schema off"
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"  wrote {os.path.relpath(dst, os.path.join(HERE, '..'))}  ({len(out)} bytes)")


if __name__ == "__main__":
    main()
