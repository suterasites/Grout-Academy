#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Grout Academy site.

Brings the sitemap pages to a clean pass on Apps/sutera-seo/checklist.py. Safe to
re-run. Tailwind-CDN site (heading tags reset by preflight, so h4 -> h3 is visually
identical).

Two page families:
  - hand pages (root + services/ + service-areas/): footer column h4 -> h3 (kills the
    H2 -> H4 skip), rewrite over-long / too-short meta descriptions and 2 titles into
    range, and add intrinsic aspect-ratio to any <img> missing width/height.
  - the /regrouting-geelong/ paid-style LP (same minimal-nav template as Apollo):
    add twitter:image, a skip-to-content link, wrap the header bar in <nav>, and a
    hero breadcrumb.

Homepage breadcrumb is deliberately left as a residual warn; the pooled score rounds
to 100.
"""

import glob
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LP = "regrouting-geelong/index.html"

TITLES = {
    "services/disability-access-rails-geelong.html": "Disability Access & Grab Rails Geelong | Grout Academy",
    "privacy.html": "Privacy Policy | Grout Academy, Geelong Regrouting",
}

METAS = {
    "index.html": "Shower regrout and tile restoration specialists across Geelong, Melbourne and Ballarat. Regrouting, waterproofing and tiling with premium Mapei. Free quotes.",
    "services.html": "Shower regrouting, pool regrouting, tile and pavement regrouting, pool coping restoration, tile repairs and waterproofing across Geelong, Melbourne and Ballarat.",
    "services/tile-and-pavement-regrouting-geelong.html": "Expert tile and pavement regrouting across Geelong, restoring stability, appearance and long-term protection. Rebuilt with premium Mapei. Free quotes.",
    "services/pool-coping-tile-restoration-geelong.html": "Specialist regrouting and restoration of pool coping tiles across Geelong, extending the life of your pool area. Rebuilt with Mapei. Free quotes.",
    "services/tile-repairs-geelong.html": "Expert tile repair services across Geelong, restoring cracked and damaged tiles without the cost of full replacement. Free quotes, workmanship guaranteed.",
    "services/disability-access-rails-geelong.html_META": "Grab rails, hand rails, shower rails and ambulant rails installed across Geelong. Safer bathrooms for older Australians, aged care and NDIS. Free quotes.",
    "service-areas/regrouting-warrnambool.html": "Regrouting in Warrnambool and the south-west coast. Shower and pool regrouting, tile repairs and waterproofing, rebuilt with Mapei. Fixed quote in writing.",
    "privacy.html_META": "How Grout Academy collects, uses, stores and protects the personal information you provide through our website and enquiries, under the Privacy Act 1988.",
}

_dim_cache = {}


def img_ratio(src, base):
    if not src or src.startswith(("http://", "https://", "data:")):
        return None
    path = os.path.normpath(os.path.join(base, src.split("?")[0]))
    if path in _dim_cache:
        return _dim_cache[path]
    r = None
    if os.path.exists(path):
        try:
            out = subprocess.check_output(
                ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                stderr=subprocess.DEVNULL).decode()
            w = re.search(r"pixelWidth:\s*(\d+)", out)
            h = re.search(r"pixelHeight:\s*(\d+)", out)
            if w and h and int(h.group(1)):
                r = f"{w.group(1)}/{h.group(1)}"
        except Exception:
            pass
    _dim_cache[path] = r
    return r


def _has_dims(tag):
    if re.search(r'\bwidth\s*=', tag) and re.search(r'\bheight\s*=', tag):
        return True
    m = re.search(r'style="([^"]*)"', tag, re.I)
    style = (m.group(1) if m else "").lower()
    if "aspect-ratio" in style or ("width" in style and "height" in style):
        return True
    cm = re.search(r'class="([^"]*)"', tag)
    cls = cm.group(1) if cm else ""
    if re.search(r"(?:^|\s)(?:aspect|size)-\S", cls):
        return True
    return bool(re.search(r"(?:^|\s)w-\S", cls) and re.search(r"(?:^|\s)h-\S", cls))


def fix_imgs(html, base):
    def rep(m):
        tag = m.group(0)
        if _has_dims(tag):
            return tag
        sm = re.search(r'src="([^"]*)"', tag)
        src = sm.group(1) if sm else ""
        if not src:
            add = "width:auto;height:auto"
        else:
            r = img_ratio(src, base)
            if not r:
                return tag
            add = f"aspect-ratio:{r}"
        st = re.search(r'style="([^"]*)"', tag)
        if st:
            new = st.group(1).rstrip(";") + ";" + add
            return tag[:st.start(1)] + new + tag[st.end(1):]
        return re.sub(r"\s*/?>$", f' style="{add}">', tag)

    return re.sub(r"<img\b[^>]*?/?>", rep, html)


def meta_for(rel):
    return METAS.get(rel + "_META", METAS.get(rel))


def patch_hand(rel):
    path = os.path.join(ROOT, rel)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    if rel in TITLES:
        h2 = re.sub(r"<title>.*?</title>", "<title>" + TITLES[rel] + "</title>",
                    html, count=1, flags=re.S)
        if h2 != html:
            html = h2
            did.append(f"title({len(TITLES[rel])})")

    new = meta_for(rel)
    if new:
        h2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                    lambda m: m.group(1) + new + m.group(2), html, count=1)
        if h2 != html:
            html = h2
            did.append(f"desc({len(new)})")

    if re.search(r"</?h4\b", html):
        html = re.sub(r"<(/?)h4(\b[^>]*)>", r"<\1h3\2>", html)
        did.append("h4->h3")

    h2 = fix_imgs(html, os.path.dirname(path))
    if h2 != html:
        html = h2
        did.append("img-dims")

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def patch_lp():
    path = os.path.join(ROOT, LP)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    # twitter:image mirrors og:image
    if 'name="twitter:image"' not in html:
        og = re.search(r'<meta property="og:image" content="([^"]*)"', html)
        if og:
            tag = f'  <meta name="twitter:image" content="{og.group(1)}">\n'
            html = re.sub(r'(<meta name="twitter:description"[^>]*>\n)', r"\1" + tag, html, count=1)
            did.append("twitter:image")

    # skip link
    if 'href="#top"' not in html or "Skip to content" not in html:
        skip = ('<a href="#top" style="position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;" '
                'onfocus="this.style.cssText=\'position:fixed;top:12px;left:12px;width:auto;height:auto;background:#0A0A0A;'
                'color:#fff;padding:8px 16px;border-radius:4px;z-index:100;text-decoration:none;font-weight:600;\'" '
                'onblur="this.style.cssText=\'position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;\'">'
                'Skip to content</a>\n')
        html = html.replace('<body class="bg-white antialiased overflow-x-hidden">',
                            '<body class="bg-white antialiased overflow-x-hidden">\n' + skip, 1)
        did.append("skip")

    # wrap the header bar div in <nav>
    if "<nav" not in html.split("</header>")[0]:
        anchor = '<div class="max-w-6xl mx-auto px-5 sm:px-8 h-16 sm:h-20 flex items-center justify-between">'
        if anchor in html:
            html = html.replace(anchor, '<nav aria-label="Primary" class="max-w-6xl mx-auto px-5 sm:px-8 h-16 sm:h-20 flex items-center justify-between">', 1)
            # close: the div closes right before </header>
            html = re.sub(r'</div>\s*</header>', '</nav>\n  </header>', html, count=1)
            did.append("nav")

    # hero breadcrumb (Apollo template hero)
    if 'aria-label="Breadcrumb"' not in html:
        anchor = '<div class="lg:col-span-7 text-white">'
        if anchor in html:
            crumb = (anchor + '\n            <nav aria-label="Breadcrumb" class="flex items-center gap-2 '
                     'text-[11px] font-medium tracking-[0.18em] uppercase text-white/40 mb-6">'
                     '<a href="../" class="hover:text-white/70">Home</a>'
                     '<span aria-hidden="true">/</span>'
                     '<span class="text-white/70">Regrouting Geelong</span></nav>')
            html = html.replace(anchor, crumb, 1)
            did.append("breadcrumb")

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    hands = []
    for pat in ("*.html", "services/*.html", "service-areas/*.html"):
        hands += glob.glob(os.path.join(ROOT, pat))
    for path in sorted(hands):
        rel = os.path.relpath(path, ROOT)
        out = patch_hand(rel)
        if out:
            print(f"  {rel:52s} {', '.join(out)}")
    print(f"  {LP:52s} {', '.join(patch_lp()) or 'no change'}")
    print("\nDone. Idempotent.")


if __name__ == "__main__":
    main()
