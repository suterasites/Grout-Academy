#!/usr/bin/env python3
"""
Build service pages for a suburb that already has Shower + Pool Regrouting pages but
not the service its searchers are actually typing.

Why this exists (WP HQ suburb move, 2026-11-13): 60 of the site's 61 pages are
indexed, and the target suburbs with zero impressions already have pages. Search
demand is concentrated where it always was, and in two of those suburbs the only
page ranking for "grout repairs <suburb>" and "tile regrouting <suburb>" is the
SHOWER page, because the service itself has no page there:

  grout repairs bacchus marsh     20 impr  #7.8  -> shower-regrouting-bacchus-marsh
  grout sealing bacchus marsh     19 impr  #5.9  -> shower-regrouting-bacchus-marsh
  tile regrouting bacchus marsh   18 impr  #5.5  -> shower-regrouting-bacchus-marsh
  tile regrouting point cook      16 impr  #4.6-30 -> /service-areas, the Wyndham hub
  (Search Console, query x page, 2026-08-15..2026-11-10)

So each page here is the missing service in a suburb that already draws the search.

The SHELL is that service's hand-written Ballarat page (2026-09-14): head chrome,
tracking, fonts, nav and footer are carried byte for byte; the SEO head block,
JSON-LD Service/FAQ/Breadcrumb and everything inside <main> come from PAGES below.
Every sentence of prose is written for its page, because the pre-push gate fails a
page that shares more than 15% of its prose with any other page.

Claims are limited to what the CRM records: Mapei-only, fixed written quote, no
call-out fee, workmanship guarantee, domestic and commercial, and (for Wyndham only)
"installer based in the Wyndham area". No job in either suburb is on record, so
the recent-work block keeps the shell's generic heading.

Run from anywhere:  python3 .build/gen_service_depth.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SERVICES = os.path.join(ROOT, "services")
BASE = "https://www.groutacademy.com.au"

SHELL = {
    "tile-repairs": "tile-repairs-ballarat.html",
    "tile-and-pavement-regrouting": "tile-and-pavement-regrouting-ballarat.html",
}
SERVICE_TYPE = {
    "tile-repairs": "Tile Repairs",
    "tile-and-pavement-regrouting": "Tile and Pavement Regrouting",
}
# Cross-sell card order in the shells, and where each card points per suburb. A card
# points at the suburb's own page when one exists, else at a named fallback suburb,
# else at the canonical Geelong page (exists for every service).
CARD_SERVICES = ["shower-regrouting", "pool-regrouting", "tile-and-pavement-regrouting",
                 "pool-coping-tile-restoration", "tile-repairs", "waterproofing-and-resilicone"]

LIST_ITEM = '        <li class="flex gap-3"><span class="text-pomegranate font-bold">✓</span> {}</li>'

PAGES = [
    # ------------------------------------------------------------------ Bacchus Marsh
    {
        "service": "tile-repairs", "slug": "bacchus-marsh", "name": "Bacchus Marsh",
        "card_fallback": {},
        "title": "Tile and Grout Repairs Bacchus Marsh | Grout Academy",
        "description": "Cracked, loose or drummy tiles and failed grout repaired in Bacchus Marsh, Darley and Maddingley. Mapei products, fixed written quote, no call-out fee.",
        "og_description": "Cracked tiles and failed grout repaired across Bacchus Marsh without re-tiling the room. Free quote.",
        "tw_description": "One cracked tile, a loose row or worn grout, fixed properly with Mapei. Free quote in Bacchus Marsh.",
        "area_served": ["City:Bacchus Marsh", "Place:Darley", "Place:Maddingley", "Place:Ballan"],
        "schema_description": "Repair of cracked, chipped, loose and drummy tiles and failed grout across Bacchus Marsh, Darley and Maddingley. Damaged tiles are replaced with a matched or closest-available tile and the surrounding grout is rebuilt with Mapei products.",
        "h1": "Tile and Grout Repairs Bacchus Marsh",
        "hero": "Cracked tiles, loose tiles and grout that has crumbled out of the joints, repaired across Bacchus Marsh, Darley and Maddingley without pulling up the whole floor.",
        "intro_h2": "Small Damage, Fixed Small",
        "intro": [
            "A cracked tile in the kitchen, a loose one beside the shower or a run of grout worn down below the tile edge does not mean a renovation. We cut out the damaged tiles, set replacements and rebuild the grout around them with Mapei, so the repair holds and the rest of the room stays exactly as it is.",
            "Bacchus Marsh is part of our regular service area, along with Darley, Maddingley and Ballan. There is no call-out fee, and the quote is a fixed price in writing before anything is touched. If a shower in the same house needs regrouting too, tell us when you enquire and we will price both together.",
        ],
        "why_h2": "Grout Fails Before Tiles Do",
        "why": [
            "Most tile damage starts in the joints. Grout wears, cracks or shrinks back from the edge, water gets in underneath, and the adhesive holding the tile slowly lets go. By the time a tile rocks underfoot, the grout around it has usually been letting water through for a long while.",
            "That is why a proper repair renews the grout around the damaged area and not just the tile in the middle of it. Patching one tile and leaving tired grout beside it is how the same spot ends up needing a second repair.",
        ],
        "local_h2": "Repairs in Bacchus Marsh Homes",
        "local": [
            "Bacchus Marsh has two kinds of housing side by side: older homes close to the town centre, and newer estates in Darley and around the edges of town. Older kitchens and bathrooms often have tiles laid straight onto render, while newer ones can have builder-grade grout that was never sealed. Both end up with cracked tiles and leaking joints, for different reasons.",
            "The valley swings from frosty winter mornings to hot summer afternoons, and tiled floors move with it. That movement opens hairline cracks in the grout first. Before a new tile goes down we check what the old one was sitting on, and if the surface underneath changes the job, we tell you and confirm the price in writing before carrying on.",
        ],
        "process_h2": "How a Tile Repair Works",
        "process_lead": "Every repair runs in the same order:",
        "process": [
            "Look over the damaged tiles and tap-test the ones around them",
            "Cut out cracked, chipped or loose tiles without disturbing their neighbours",
            "Clean back and level the surface underneath",
            "Bed a matched or closest-available replacement tile",
            "Rebuild the surrounding grout with Mapei and seal the area",
        ],
        "signs_h2": "When to Call for a Repair",
        "signs_lead": "Get it looked at if you see:",
        "signs": [
            "Grout that has cracked, crumbled or dropped below the tile edge",
            "A tile that moves, rocks or sounds hollow when tapped",
            "A crack running across the face of a tile",
            "Chipped tile edges in a hallway or kitchen",
            "Lifting tiles on a patio, step or alfresco area",
        ],
        "choose_h2": "What Every Repair Includes",
        "choose_lead": "On every Bacchus Marsh tile repair:",
        "choose": [
            "Mapei grout, silicone and waterproofing products",
            "A fixed quote in writing before work starts",
            "No call-out fee",
            "Homes and commercial premises",
            "Workmanship guaranteed. If something is not right, we come back and sort it",
        ],
        "cta_h2": "Cracked Tile or Crumbling Grout",
        "cta": "Call us or send an enquiry for a free quote anywhere in Bacchus Marsh, Darley or Maddingley.",
        "faq_h2": "Tile and Grout Repair Questions",
        "faq": [
            ("Can you repair the grout without replacing any tiles?",
             "Yes, if the tiles themselves are sound. Where the grout has cracked or worn but the tiles are still firmly bonded, we rake out the failed grout and rebuild the joints with Mapei. If any tiles turn out to be loose once the old grout is out, we tell you before going any further."),
            ("Can one cracked tile be replaced on its own?",
             "Usually. A damaged tile can be cut out without lifting the tiles around it, and the new one is bedded, grouted and sealed in place. The only real limit is finding a tile that matches."),
            ("What if I cannot find a matching tile?",
             "Older tiles often go out of production. We look for a match first, and if there is none we go through the nearest options with you before anything is laid. Spare tiles from the original job are the best match there is, so check the garage or the shed before we start."),
            ("How long does a tile repair take?",
             "A small repair of a few tiles is usually done in one visit. Larger areas, or repairs where the surface underneath needs work, are quoted on inspection with a timeline attached."),
            ("Do you come out to Darley, Maddingley and Ballan?",
             "Yes. Bacchus Marsh and the towns around it, including Darley, Maddingley and Ballan, are inside our service area. There is no call-out fee, and you get a fixed price in writing before any work starts."),
            ("Should I repair or re-tile?",
             "Repair when the damage is limited to a few tiles or a patch of grout. If most of a floor is cracked or drummy, fixing it tile by tile costs more than it saves, and we will say so when we see it rather than sell you a repair that will not last."),
        ],
    },
    {
        "service": "tile-and-pavement-regrouting", "slug": "bacchus-marsh", "name": "Bacchus Marsh",
        "card_fallback": {},
        "title": "Tile Regrouting and Grout Sealing Bacchus Marsh | Grout Academy",
        "description": "Tiled floors, patios, paths and driveways regrouted and sealed across Bacchus Marsh and Darley. Failed joints rebuilt with Mapei. Fixed quote, no call-out fee.",
        "og_description": "Tiled floors, patios and paving regrouted and sealed across Bacchus Marsh with Mapei grout systems. Free quote.",
        "tw_description": "Worn, cracked and weedy joints rebuilt and sealed with Mapei. Free quote across Bacchus Marsh.",
        "area_served": ["City:Bacchus Marsh", "Place:Darley", "Place:Maddingley", "Place:Ballan"],
        "schema_description": "Tile and pavement regrouting and grout sealing for indoor tiled floors, alfresco areas, patios, paths, driveways and commercial paved areas across Bacchus Marsh. Failed grout is removed and the joints are rebuilt with Mapei grout systems.",
        "h1": "Tile and Pavement Regrouting Bacchus Marsh",
        "hero": "Worn, cracked and weed-filled joints rebuilt and sealed on tiled floors, patios, paths and driveways across Bacchus Marsh, Darley and Maddingley.",
        "intro_h2": "Rebuild the Joints, Save the Surface",
        "intro": [
            "Tiles and pavers are only as solid as the grout holding them apart. Once the joints crack, wash out or sink below the edge, water gets underneath, edges start to chip and weeds take hold. We strip the failed grout out of indoor floors, alfresco areas, paths and driveways across Bacchus Marsh and rebuild every joint with Mapei grout systems.",
            "Sealing is part of the job, not an extra visit. Where a floor or an outdoor area needs protection from water and staining, the new grout is sealed once it has cured. Bacchus Marsh is in our regular service area, there is no call-out fee, and paving is quoted on the size of the area and the state of the old joints.",
        ],
        "why_h2": "Hot Summers, Frosty Mornings",
        "why": [
            "Outdoor tiles and pavers in Bacchus Marsh go from baking in January to frost in July. Every swing moves the surface a little, and old unsealed grout cannot move with it. It cracks, rain gets in, and each cold snap widens the gap, so a patio that only looks tired one winter can have loose tiles not long after.",
            "Inside the house the wear is quieter. Kitchen, hallway and laundry floors lose grout to foot traffic and mopping until the joints sit low and hold dirt that nothing will lift. Regrouting at that stage brings the floor back without lifting a single tile.",
        ],
        "process_h2": "How We Regrout Floors and Paving",
        "process_lead": "The order never changes:",
        "process": [
            "Rake out the cracked and crumbling grout",
            "Pull weeds, moss and dirt out of every joint",
            "Wash down the surface and let it dry",
            "Pack the joints with Mapei grout systems",
            "Seal the new grout where the area needs it",
            "Walk the finished surface and check every line",
        ],
        "signs_h2": "Signs It Is Time to Regrout",
        "signs_lead": "Look for:",
        "signs": [
            "Joints that have cracked, sunk or emptied out",
            "Weeds and moss pushing up between pavers",
            "Tiles or pavers that click or rock underfoot",
            "Dark grout lines that stay dirty after a scrub",
            "Water sitting in the joints after rain",
        ],
        "choose_h2": "Why Grout Academy",
        "choose_lead": "On every Bacchus Marsh floor and paving job:",
        "choose": [
            "Mapei grout systems in every joint",
            "Indoor floors, patios, paths and driveways",
            "Homes and commercial paved areas",
            "Fixed written quote, no call-out fee",
            "Workmanship guaranteed",
        ],
        "cta_h2": "Ready to Fix Those Joints",
        "cta": "Call us or send an enquiry for a free quote on your Bacchus Marsh floor, patio or driveway.",
        "faq_h2": "Floor and Paving Regrouting Questions",
        "faq": [
            ("Do you seal the grout after regrouting?",
             "Where the area needs it, yes. Outdoor paving and floors that see a lot of water or spills have the new grout sealed once it has cured, which helps keep water and staining out of the joints. The quote says whether your surface needs it."),
            ("Can you regrout paving with weeds growing through it?",
             "Yes. The weeds come out with the old grout, roots and all, and the joints are cleaned back before new grout goes in. Once a joint is full and sound again, there is nowhere left for seeds to settle."),
            ("What if my pavers have sunk or lifted?",
             "Grout fills the gap between pavers. It cannot raise one that has dropped because the base underneath has moved. If that is what is going on, we point it out at the quote rather than grout over a problem that will come back."),
            ("Can outdoor regrouting be done in winter?",
             "New grout needs dry weather to cure, so outdoor work is booked around the forecast and a wet stretch can push it back. Indoor floors can be done any time of year."),
            ("How is a floor or paving job priced?",
             "On the size of the area, how far the old joints have broken down, and whether sealing is needed. We look at it first and give you a fixed price in writing, so there is nothing to guess."),
            ("Do you cover Darley, Maddingley and Ballan?",
             "Yes. Bacchus Marsh, Darley, Maddingley, Ballan and the surrounding Moorabool area are all part of our service area, with no call-out fee."),
        ],
    },
    # ------------------------------------------------------------------ Point Cook
    {
        "service": "tile-and-pavement-regrouting", "slug": "point-cook", "name": "Point Cook",
        # no pool page in Point Cook: the Wyndham pool page is Werribee's
        "card_fallback": {"pool-regrouting": "werribee"},
        "title": "Tile Regrouting Point Cook | Floors and Alfresco | Grout Academy",
        "description": "Tiled floors, alfresco areas, patios and paths regrouted across Point Cook with Mapei grout systems. Installer based in Wyndham. Fixed quote, no call-out fee.",
        "og_description": "Tiled floors, alfresco areas and paving regrouted across Point Cook with Mapei. Installer based locally. Free quote.",
        "tw_description": "Cracked and worn joints on floors, patios and alfresco areas rebuilt with Mapei. Free quote in Point Cook.",
        "area_served": ["City:Point Cook", "Place:Williams Landing", "Place:Werribee", "Place:Hoppers Crossing"],
        "area_served_business": ["City:Melbourne", "City:Geelong", "City:Ballarat", "City:Warrnambool",
                                 "Place:Bellarine Peninsula", "Place:Surf Coast"],
        "schema_description": "Tile and pavement regrouting for indoor tiled floors, alfresco areas, patios, paths and commercial paved areas across Point Cook and Wyndham. Failed grout is removed and the joints are rebuilt with Mapei grout systems.",
        "h1": "Tile and Pavement Regrouting Point Cook",
        "hero": "Cracked, sunken and stained joints rebuilt on tiled floors, alfresco areas, patios and paths across Point Cook, Williams Landing and the rest of Wyndham.",
        "intro_h2": "Floors That Look New Again",
        "intro": [
            "Plenty of Point Cook homes have tile almost everywhere: open-plan living areas, hallways, laundries and a tiled alfresco out the back. That is a lot of grout, and it is usually the first thing to go. We rake out the joints that have cracked, stained or worn low and rebuild them with Mapei grout systems, which brings a floor back without lifting the tiles.",
            "We have an installer based in the Wyndham area, which makes Point Cook local work rather than a trip, and there is no call-out fee. Every job is quoted at a fixed price in writing once we have seen the floor or the paving.",
        ],
        "why_h2": "Bay Wind, Busy Floors",
        "why": [
            "Point Cook sits right on Port Phillip Bay, and outdoor tiling here takes wind, rain and summer heat with very little shelter. Alfresco tiles and paths dry out, soak and dry out again, and the grout between them shrinks and cracks long before the tiles give up. Once a joint opens, water gets under the tile edges and they start to chip or lift.",
            "Inside, the wear comes from traffic. Hallways, kitchens and living areas lose grout to daily mopping and foot traffic until the lines sit below the tiles, collect grime and stay dark however often they are cleaned. Regrouting puts a clean, full joint back in, and it is a much smaller job than re-tiling the room.",
        ],
        "local_h2": "Builder-Grade Grout in Newer Estates",
        "local": [
            "Many Point Cook homes were finished by volume builders, and the grout in their floors was the standard product on the day, often never sealed. A decade or more on, that grout is porous, stained and starting to crack, even where the tiles themselves are perfectly fine. It is a regrouting job, not a renovation.",
            "Weeds and moss in a tiled path or a paved side passage are the outdoor version of the same problem. They only grow where the grout has failed, so pulling them out never lasts. Fill the joint properly and there is nowhere for them to come back.",
        ],
        "process_h2": "How a Floor or Paving Regrout Runs",
        "process_lead": "Every job follows the same steps:",
        "process": [
            "Rake out the cracked, stained and crumbling grout",
            "Clear weeds, moss and grime from every joint",
            "Clean the surface and let it dry",
            "Rebuild the joints with Mapei grout systems",
            "Seal the new grout where the area calls for it",
            "Check every line before we pack up",
        ],
        "signs_h2": "Signs Your Floor or Paving Needs Regrouting",
        "signs_lead": "Watch for:",
        "signs": [
            "Grout lines that have gone dark and will not come clean",
            "Joints sitting lower than the tile edge",
            "Cracks running along the grout between tiles",
            "Weeds or moss between outdoor tiles or pavers",
            "Tile edges chipping where the grout has gone",
        ],
        "choose_h2": "Why Grout Academy",
        "choose_lead": "On every Point Cook floor and paving job:",
        "choose": [
            "Mapei grout systems in every joint",
            "Installer based in the Wyndham area",
            "Indoor floors, alfresco areas, patios and paths",
            "Fixed quote in writing, no call-out fee",
            "Workmanship guaranteed",
        ],
        "cta_h2": "Ready to Fix Your Floor",
        "cta": "Call us or send an enquiry for a free quote on your Point Cook floor, alfresco area or path.",
        "faq_h2": "Point Cook Floor and Paving Questions",
        "faq": [
            ("Can you regrout a tiled alfresco area?",
             "Yes. Alfresco tiles take the weather, so their grout tends to fail sooner than the floors inside. We strip out the old joints, rebuild them with Mapei grout systems and seal them where the area needs it, so rain and spills stay on top of the surface instead of soaking in underneath."),
            ("Will regrouting fix grout that stays dark after cleaning?",
             "Yes. Grout that stays dark has soaked up dirt and moisture deep into the joint, and no amount of scrubbing gets it out. Taking that grout out and putting new grout in is what brings the lines back to their original colour."),
            ("What if some of my tiles are loose or cracked?",
             "We check every tile as the old grout comes out. Loose or cracked ones can be lifted and replaced as part of the same job, and if that changes the price, we confirm it with you in writing first."),
            ("How long will my floor take?",
             "That depends on the size of the area and the state of the old grout. An ensuite floor and a whole open-plan living area are very different jobs, so the timeline comes with your quote rather than as a guess."),
            ("Do you regrout commercial floors?",
             "Yes. We regrout commercial tiled floors and paved areas as well as homes. Send through the rough size of the area and what it is used for, and we will quote it on that."),
            ("Do you cover the rest of Wyndham?",
             "Yes. Point Cook, Williams Landing, Werribee, Tarneit, Hoppers Crossing and the rest of the City of Wyndham are inside our service area, and our installer is based locally."),
        ],
    },
]


def page_url(service, slug, html=True):
    return f"{BASE}/services/{service}-{slug}" + (".html" if html else "")


def areas(spec):
    out = []
    for item in spec:
        kind, name = item.split(":", 1)
        out.append({"@type": kind, "name": name})
    return out


def card_target(card_service, page):
    """Suburb slug a cross-sell card should point at."""
    for slug in (page["slug"], page["card_fallback"].get(card_service), "geelong"):
        if slug and os.path.exists(os.path.join(SERVICES, f"{card_service}-{slug}.html")):
            return slug
        if slug == page["slug"] and any(p["service"] == card_service and p["slug"] == slug for p in PAGES):
            return slug  # built in this run
    raise AssertionError(f"{card_service}: no page to point at")


def build_head(head, page):
    service, slug, name = page["service"], page["slug"], page["name"]
    title = page["title"]
    subs = [
        (r"<title>.*?</title>", f"<title>{title}</title>"),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{page["description"]}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{page_url(service, slug, html=False)}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{page["og_description"]}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{page_url(service, slug)}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{page["tw_description"]}">'),
        (r'<meta name="geo.placename" content="[^"]*">', f'<meta name="geo.placename" content="{name}">'),
    ]
    for pat, rep in subs:
        head, n = re.subn(pat, lambda m, r=rep: r, head, count=1, flags=re.S)
        assert n == 1, f"{service}-{slug}: head field {pat} not found in shell"

    m = re.search(r'(?s)(<script type="application/ld\+json">)(.*?)(</script>)', head)
    graph = json.loads(m.group(2))
    for node in graph["@graph"]:
        t = node["@type"]
        if t == "LocalBusiness" and page.get("area_served_business"):
            node["areaServed"] = areas(page["area_served_business"])
        elif t == "Service":
            node.update({
                "name": f"{SERVICE_TYPE[service]} {name}",
                "serviceType": SERVICE_TYPE[service],
                "areaServed": areas(page["area_served"]),
                "description": page["schema_description"],
                "url": page_url(service, slug),
            })
        elif t == "FAQPage":
            node["mainEntity"] = [{"@type": "Question", "name": q,
                                   "acceptedAnswer": {"@type": "Answer", "text": a}}
                                  for q, a in page["faq"]]
        elif t == "BreadcrumbList":
            node["itemListElement"][-1].update({"name": page["h1"], "item": page_url(service, slug)})
    ld = "\n" + json.dumps(graph, indent=2, ensure_ascii=False) + "\n  "
    return head[:m.start(2)] + ld + head[m.end(2):]


def section_text(h2, paras, bg, last_mb=True):
    ps = []
    for i, p in enumerate(paras):
        cls = "text-ink-soft text-lg" + (" mb-4" if i < len(paras) - 1 else "")
        ps.append(f'      <p class="{cls}">{p}</p>')
    return (f'  <section class="py-20 lg:py-28 {bg}">\n'
            f'    <div class="max-w-[900px] mx-auto px-5 lg:px-8">\n'
            f'      <h2 class="heading-uppercase text-4xl md:text-6xl font-display mb-6">{h2}</h2>\n'
            + "\n".join(ps) + "\n    </div>\n  </section>\n")


def section_list(h2, lead, items, bg):
    lis = "\n".join(LIST_ITEM.format(i) for i in items)
    return (f'  <section class="py-20 lg:py-28 {bg}">\n'
            f'    <div class="max-w-[900px] mx-auto px-5 lg:px-8">\n'
            f'      <h2 class="heading-uppercase text-4xl md:text-6xl font-display mb-6">{h2}</h2>\n'
            f'      <p class="text-ink-soft text-lg mb-6">{lead}</p>\n'
            f'      <ul class="space-y-3 text-ink-soft text-lg">\n{lis}\n      </ul>\n'
            f'    </div>\n  </section>\n')


def build_main(main, page):
    service, name = page["service"], page["name"]

    def between(a, b):
        return main[main.index(a):main.index(b)]

    breadcrumb = between("<!-- BREADCRUMB -->", "<!-- HERO -->")
    breadcrumb = re.sub(r'(<li aria-current="page" class="text-ink font-medium">).*?(</li>)',
                        lambda m: m.group(1) + page["h1"] + m.group(2), breadcrumb, count=1)

    hero = between("<!-- HERO -->", "<!-- INTRO -->")
    hero = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + page["h1"] + m.group(2), hero, count=1)
    hero = re.sub(r'(<p class="text-lg md:text-xl text-ink-soft mb-8 max-w-2xl mx-auto">).*?(</p>)',
                  lambda m: m.group(1) + page["hero"] + m.group(2), hero, count=1)

    intro = between("<!-- INTRO -->", "<!-- WHY IT MATTERS -->")
    img = re.search(r"(?s)<div>\s*<img .*?</div>", intro).group(0)
    intro = ("<!-- INTRO -->\n"
             '  <section class="py-20 lg:py-28 bg-ink-bg">\n'
             '    <div class="max-w-[1280px] mx-auto px-5 lg:px-8 grid lg:grid-cols-2 gap-12 items-center">\n'
             "      <div>\n"
             f'        <h2 class="heading-uppercase text-4xl md:text-6xl font-display mb-6">{page["intro_h2"]}</h2>\n'
             f'        <p class="text-ink-soft text-lg mb-4">{page["intro"][0]}</p>\n'
             f'        <p class="text-ink-soft text-lg">{page["intro"][1]}</p>\n'
             "      </div>\n"
             f"      {img}\n"
             "    </div>\n  </section>\n\n  ")

    # Alternate the band colours from here on, starting white after the grey intro.
    bands = iter(["bg-white", "bg-ink-bg"] * 4)
    parts = ["<!-- WHY IT MATTERS -->\n" + section_text(page["why_h2"], page["why"], next(bands))]
    if page.get("local"):
        parts.append("<!-- LOCAL -->\n" + section_text(page["local_h2"], page["local"], next(bands)))
    parts.append("<!-- PROCESS -->\n" + section_list(page["process_h2"], page["process_lead"], page["process"], next(bands)))
    parts.append("<!-- SIGNS -->\n" + section_list(page["signs_h2"], page["signs_lead"], page["signs"], next(bands)))
    parts.append("<!-- WHY CHOOSE -->\n" + section_list(page["choose_h2"], page["choose_lead"], page["choose"], next(bands)))
    body_bands = "\n  ".join(parts) + "\n  "

    cross = between("<!-- CROSS-SELL GRID -->", "<!-- RECENT WORK -->")
    cross = cross.replace("Services in Ballarat", f"Services in {name}")
    cross_bg = next(bands)
    cross = re.sub(r'<section class="py-20 lg:py-28 bg-[a-z-]+">', f'<section class="py-20 lg:py-28 {cross_bg}">', cross, count=1)

    def retarget(m):
        card_service = m.group(1)
        return f'href="{card_service}-{card_target(card_service, page)}.html" class="block bg-white border'
    cross = re.sub(r'href="([a-z-]+?)-(?:ballarat|geelong)\.html" class="block bg-white border', retarget, cross)

    recent = between("<!-- RECENT WORK -->", "<!-- CTA -->")
    assert "Recent Finished Jobs" in recent, "shell recent-work heading changed"

    cta = between("<!-- CTA -->", "<!-- FAQS -->")
    cta = re.sub(r'(<h2 class="heading-uppercase text-4xl md:text-5xl font-display text-white mb-2">).*?(</h2>)',
                 lambda m: m.group(1) + page["cta_h2"] + m.group(2), cta, count=1)
    cta = re.sub(r'(<p class="text-white/90 text-lg">).*?(</p>)', lambda m: m.group(1) + page["cta"] + m.group(2), cta, count=1)

    faqs = main[main.index("<!-- FAQS -->"):]
    svg = re.search(r"(?s)<svg class=\"faq-chevron.*?</svg>", faqs).group(0)
    items = "\n".join(
        '        <details class="faq-item border border-ink-line rounded-lg p-5"><summary '
        f'class="flex items-center justify-between font-semibold text-lg">{q}{svg}</summary>'
        f'<p class="mt-4 text-ink-soft">{a}</p></details>'
        for q, a in page["faq"])
    faqs = re.sub(r'(<h2 class="heading-uppercase text-4xl md:text-6xl font-display mb-3">).*?(</h2>)',
                  lambda m: m.group(1) + page["faq_h2"] + m.group(2), faqs, count=1)
    faqs = re.sub(r'(?s)(<div class="space-y-3">\n).*?(\n      </div>)', lambda m: m.group(1) + items + m.group(2), faqs, count=1)
    faq_bg = next(bands)
    faqs = re.sub(r'<section class="py-20 lg:py-28 bg-[a-z-]+">', f'<section class="py-20 lg:py-28 {faq_bg}">', faqs, count=1)

    head_of_main = main[:main.index("<!-- BREADCRUMB -->")]
    return head_of_main + breadcrumb + hero + intro + body_bands + cross + recent + cta + faqs


def build(page):
    shell_path = os.path.join(SERVICES, SHELL[page["service"]])
    html = open(shell_path, encoding="utf-8").read()
    b = html.index("<body")
    ms, me = html.index("<main"), html.index("</main>")
    out = build_head(html[:b], page) + html[b:ms] + build_main(html[ms:me], page) + html[me:]

    service, slug, name = page["service"], page["slug"], page["name"]
    tag = f"{service}-{slug}"
    pre = out[:out.index("<!-- FOOTER -->")]
    assert "Ballarat" not in pre[pre.index("<main"):], f"{tag}: Ballarat left in the page body"
    assert "ballarat.html" not in pre, f"{tag}: link to a Ballarat page left in"
    assert out.count("SUTERA_LEAD_EVENTS") == 1, f"{tag}: lead-events snippet altered"
    assert "AW-17960926932" in out and "G-K7M7GWT3RJ" in out, f"{tag}: tracking IDs dropped"
    assert out.count("<h1") == 1 and name in out, f"{tag}: H1 or suburb missing"
    assert "—" not in out and "–" not in out, f"{tag}: em or en dash in output"
    for q, a in page["faq"]:
        assert q in out and a in out, f"{tag}: FAQ not rendered: {q}"
    json.loads(re.search(r'(?s)<script type="application/ld\+json">(.*?)</script>', out).group(1))
    for href in re.findall(r'href="([a-z0-9-]+\.html)" class="block bg-white border', out):
        assert os.path.exists(os.path.join(SERVICES, href)) or href == f"{tag}.html" or \
            any(f"{p['service']}-{p['slug']}.html" == href for p in PAGES), f"{tag}: card 404s: {href}"
    return out


def main():
    for page in PAGES:
        dst = os.path.join(SERVICES, f"{page['service']}-{page['slug']}.html")
        out = build(page)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"  wrote services/{page['service']}-{page['slug']}.html")
    print(f"[gen] wrote {len(PAGES)} pages")


if __name__ == "__main__":
    main()
