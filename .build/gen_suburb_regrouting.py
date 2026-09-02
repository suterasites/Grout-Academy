#!/usr/bin/env python3
"""
Generate Shower Regrouting + Pool Regrouting pages for every Grout Academy suburb
that doesn't already have them, by cloning the canonical Geelong service pages and
surgically localising them.

Nav, footer, GA/gtag, SUTERA_LEAD_EVENTS, styles and images are preserved
byte-for-byte. The nav + footer + the 4 OTHER cross-sell cards keep pointing at the
canonical -geelong.html service pages (those exist site-wide; the new suburbs only
have shower + pool, so localising them would 404). Only the head SEO block, schema
areaServed (primary), breadcrumb, H1, hero, intro, region phrases, the shower<->pool
cross-sell link, the recent-work heading, plus a per-suburb local paragraph and FAQ
are changed. Each suburb gets a genuine local angle so the pages are not thin
name-swaps.

Run from anywhere:  python3 .build/gen_suburb_regrouting.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SERVICES = os.path.normpath(os.path.join(HERE, "..", "services"))

# service slug -> the sibling service its cross-sell grid links to (must be localised)
SERVICE_SIBLING = {
    "shower-regrouting": "pool-regrouting",
    "pool-regrouting": "shower-regrouting",
}

COASTAL = ("{name} sits on the coast, where salt air and sea humidity work against grout "
           "and silicone every day. Sealed joints break down faster near the water than they "
           "do inland, so staying on top of regrouting and resiliconing keeps water where it "
           "belongs and protects your tiles.")
GOLDFIELDS = ("{name} runs through cold, wet winters and warm, dry summers, and that constant "
              "movement is hard on grout. Tiles expand and contract, hairline cracks open up, "
              "and water works its way in behind them. Regular regrouting keeps the seal intact "
              "through the seasonal swings.")
GROWTH = ("{name} is a mix of established homes and fast-growing new estates, and both throw up "
          "grout problems: older showers that have simply worn out, and new bathrooms where the "
          "original waterproofing was rushed. We regrout and reseal both properly, so the water "
          "stays where it should.")

CLIMATE_LINE = {
    "coastal": ("Coastal salt air breaks grout and silicone down faster here, so regular "
                "regrouting and resiliconing matters more near the water."),
    "goldfields": ("The cold winters and seasonal movement are hard on grout, so keeping it "
                   "sealed and intact matters."),
    "growth": ("Between older homes and rushed new-build bathrooms, there is plenty that needs "
               "regrouting and resealing done properly."),
}

# name        = display name (title, H1, breadcrumb, geo, primary areaServed)
# region      = the "across ..." phrase used in the hero + intro (suburb + 2 real neighbours)
# group       = local-angle paragraph + climate line
# faq_towns   = towns named in the local FAQ answer
# faq_region  = the wider region named in the local FAQ answer
SUBURBS = [
    {"slug": "ballarat", "name": "Ballarat", "group": "goldfields",
     "region": "Ballarat, Ballan and Bacchus Marsh",
     "faq_towns": "Ballan, Bacchus Marsh, Bannockburn and Buninyong", "faq_region": "Ballarat region and central goldfields"},
    {"slug": "bacchus-marsh", "name": "Bacchus Marsh", "group": "goldfields",
     "region": "Bacchus Marsh, Ballan and Melton",
     "faq_towns": "Ballan, Melton, Darley and Maddingley", "faq_region": "Moorabool and western corridor"},
    {"slug": "ballan", "name": "Ballan", "group": "goldfields",
     "region": "Ballan, Ballarat and Bacchus Marsh",
     "faq_towns": "Ballarat, Bacchus Marsh, Gordon and Myrniong", "faq_region": "Moorabool and Ballarat region"},
    {"slug": "werribee", "name": "Werribee", "group": "growth",
     "region": "Werribee, Wyndham Vale and Point Cook",
     "faq_towns": "Wyndham Vale, Point Cook, Hoppers Crossing and Tarneit", "faq_region": "Wyndham area"},
    {"slug": "lara", "name": "Lara", "group": "growth",
     "region": "Lara, Geelong and Little River",
     "faq_towns": "Geelong, Little River, Corio and Norlane", "faq_region": "northern Geelong area"},
    {"slug": "bellarine", "name": "Bellarine", "group": "coastal",
     "region": "the Bellarine Peninsula, Ocean Grove and Drysdale",
     "faq_towns": "Ocean Grove, Drysdale, Barwon Heads and Portarlington", "faq_region": "Bellarine Peninsula"},
    {"slug": "bannockburn", "name": "Bannockburn", "group": "goldfields",
     "region": "Bannockburn, Teesdale and Geelong",
     "faq_towns": "Teesdale, Inverleigh, Batesford and Geelong", "faq_region": "Golden Plains and Geelong region"},
    {"slug": "lorne", "name": "Lorne", "group": "coastal",
     "region": "Lorne, Anglesea and Apollo Bay",
     "faq_towns": "Anglesea, Aireys Inlet, Apollo Bay and the Surf Coast towns", "faq_region": "Surf Coast"},
    {"slug": "apollo-bay", "name": "Apollo Bay", "group": "coastal",
     "region": "Apollo Bay, Lorne and Marengo",
     "faq_towns": "Lorne, Marengo, Skenes Creek and the Otway coast towns", "faq_region": "Otway coast"},
    {"slug": "colac", "name": "Colac", "group": "goldfields",
     "region": "Colac, Birregurra and Winchelsea",
     "faq_towns": "Birregurra, Winchelsea, Elliminyt and the Otway hinterland", "faq_region": "Colac Otway area"},
    {"slug": "port-fairy", "name": "Port Fairy", "group": "coastal",
     "region": "Port Fairy, Warrnambool and Koroit",
     "faq_towns": "Warrnambool, Koroit, Yambuk and the South-West coast towns", "faq_region": "South-West coast"},
    {"slug": "portland", "name": "Portland", "group": "coastal",
     "region": "Portland, Heywood and Port Fairy",
     "faq_towns": "Heywood, Port Fairy, Cape Bridgewater and Narrawong", "faq_region": "far South-West coast"},
    {"slug": "teesdale", "name": "Teesdale", "group": "goldfields",
     "region": "Teesdale, Bannockburn and Inverleigh",
     "faq_towns": "Bannockburn, Inverleigh, Shelford and Meredith", "faq_region": "Golden Plains region"},
    {"slug": "rokewood", "name": "Rokewood", "group": "goldfields",
     "region": "Rokewood, Bannockburn and Meredith",
     "faq_towns": "Bannockburn, Meredith, Cressy and Shelford", "faq_region": "Golden Plains region"},
]


def local_para_html(sub):
    tmpl = {"coastal": COASTAL, "goldfields": GOLDFIELDS, "growth": GROWTH}[sub["group"]]
    return '<p class="text-ink-soft text-lg">' + tmpl.format(name=sub["name"]) + '</p>'


def local_faq(sub):
    q = f"Do you service {sub['name']} and the surrounding area?"
    a = (f"Yes. We cover {sub['name']}, {sub['faq_towns']}, and the wider {sub['faq_region']}. "
         f"{CLIMATE_LINE[sub['group']]} Contact us for a free quote anywhere in the area.")
    faq_json = ('{ "@type": "Question", "name": "' + q + '", "acceptedAnswer": { "@type": "Answer", '
                '"text": "' + a + '" }},')
    faq_html = (
        '<details class="faq-item border border-ink-line rounded-lg p-5"><summary '
        'class="flex items-center justify-between font-semibold text-lg">' + q +
        '<svg class="faq-chevron w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path '
        'fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 '
        '111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" '
        'clip-rule="evenodd"/></svg></summary><p class="mt-4 text-ink-soft">' + a + '</p></details>'
    )
    return faq_json, faq_html


def transform(html, service, sub):
    name, slug = sub["name"], sub["slug"]
    region = sub["region"]
    sibling = SERVICE_SIBLING[service]

    b = html.index("<body")
    head, body = html[:b], html[b:]

    # HEAD: self URLs to this page, then blanket display + primary areaServed -> suburb.
    # see gen_warrnambool_services.py: canonicals are clean URLs since 2026-09-02,
    # so the .html form alone no longer matches the canonical
    head = head.replace("-geelong.html", f"-{slug}.html")
    head = head.replace('-geelong"', f'-{slug}"')
    head = head.replace("Geelong", name)

    # BODY: keep the footer identical to the rest of the site.
    f = body.index("<!-- FOOTER -->")
    pre, foot = body[:f], body[f:]

    # Region phrases FIRST (they carry the full "Geelong, Warrnambool and Ballarat" list;
    # swap the whole phrase so the suburb's own region text lands cleanly).
    pre = pre.replace("Geelong, Warrnambool, Ballarat and surrounding regions", f"{region} and surrounding regions")
    pre = pre.replace("Geelong, Warrnambool and Ballarat", region)
    pre = pre.replace("Geelong and surrounding regions", f"{name} and surrounding regions")  # pool's short intro
    # Localise ONLY the sibling cross-sell card (unique "block bg-white border" class);
    # nav, footer and the other 4 cards keep their canonical -geelong.html targets.
    pre = pre.replace(
        f'{sibling}-geelong.html" class="block bg-white border',
        f'{sibling}-{slug}.html" class="block bg-white border',
    )
    # Surgical (NOT blanket): localise only the template's own "Geelong" spots. A blanket
    # swap would also clobber a legitimate neighbour reference (e.g. Lara / Bannockburn
    # genuinely list Geelong as a nearby town in their region phrase + local FAQ).
    pre = pre.replace("Regrouting Geelong", f"Regrouting {name}")   # H1 + breadcrumb
    pre = pre.replace("Services in Geelong", f"Services in {name}")  # cross-sell heading
    pre = pre.replace("Across Geelong", f"Across {name}")            # recent-work heading

    html = head + pre + foot

    # Inject the local angle paragraph right after the intro paragraph (unique mb-4 class).
    html = re.sub(
        r'(<p class="text-ink-soft text-lg mb-4">.*?</p>)',
        lambda m: m.group(1) + "\n        " + local_para_html(sub),
        html, count=1, flags=re.S,
    )
    # Inject the local FAQ first, in both the schema graph and the visible list.
    faq_json, faq_html = local_faq(sub)
    html = html.replace('"mainEntity": [\n          ', '"mainEntity": [\n          ' + faq_json + '\n          ', 1)
    html = html.replace('<details class="faq-item', faq_html + '\n        <details class="faq-item', 1)
    return html


def main():
    wrote = 0
    for service in SERVICE_SIBLING:
        src = os.path.join(SERVICES, f"{service}-geelong.html")
        with open(src, encoding="utf-8") as fh:
            ref = fh.read()
        for sub in SUBURBS:
            out = transform(ref, service, sub)
            # Guards: the template's own "Geelong" spots must be localised. (Legitimate
            # neighbour references to Geelong in the region phrase / local FAQ are allowed.)
            assert "Regrouting Geelong" not in out, f"{service}-{sub['slug']}: H1/breadcrumb not localised"
            assert "Services in Geelong" not in out, f"{service}-{sub['slug']}: cross-sell heading not localised"
            assert "Across Geelong" not in out, f"{service}-{sub['slug']}: recent-work heading not localised"
            assert "-geelong.html" not in out[:out.index("<body")], f"{service}-{sub['slug']}: geelong slug left in head"
            assert sub["name"] in out, f"{service}-{sub['slug']}: no suburb text"
            assert out.count("SUTERA_LEAD_EVENTS") == 1, f"{service}-{sub['slug']}: lead-events snippet altered"
            assert "AW-17960926932" in out and "G-K7M7GWT3RJ" in out, f"{service}-{sub['slug']}: tracking IDs dropped"
            # the sibling cross-sell link must resolve to the new suburb (page we also write)
            assert f'{SERVICE_SIBLING[service]}-{sub["slug"]}.html" class="block bg-white border' in out, \
                f"{service}-{sub['slug']}: sibling cross-sell not localised"
            dst = os.path.join(SERVICES, f"{service}-{sub['slug']}.html")
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(out)
            wrote += 1
            print(f"  wrote services/{service}-{sub['slug']}.html")
    print(f"[gen] wrote {wrote} pages")


if __name__ == "__main__":
    main()
