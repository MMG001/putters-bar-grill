#!/usr/bin/env python3
"""
JSON-LD entity-graph builder for puttersverona.com  (v2 spec)

- One <script type="application/ld+json"> per page, one @graph, @id-linked.
- Business facts live in CONFIG below. The menu is parsed from menu.html
  (the HTML is this static site's data source) so menu edits regenerate
  automatically.
- Run:  python3 tools/schema.py          (regenerates + injects + checks)
        python3 tools/schema.py --check  (integrity check only)

Injected between markers:
  <!-- BEGIN JSON-LD SCHEMA --> ... <!-- END JSON-LD SCHEMA -->
so re-running is idempotent. Do not hand-edit the injected block.
"""
import json, re, sys, html, subprocess
from pathlib import Path

def git_dates(fname):
    """(datePublished, dateModified) from git history; (None, None) if unavailable."""
    try:
        pub = subprocess.run(["git", "log", "--diff-filter=A", "--follow",
                              "--format=%cI", "--", fname], cwd=str(Path(__file__).resolve().parent.parent),
                             capture_output=True, text=True).stdout.strip().splitlines()
        mod = subprocess.run(["git", "log", "-1", "--format=%cI", "--", fname],
                             cwd=str(Path(__file__).resolve().parent.parent),
                             capture_output=True, text=True).stdout.strip()
        return (pub[-1] if pub else None), (mod or None)
    except Exception:
        return None, None

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://puttersverona.com"

# ---------------------------------------------------------------- CONFIG
BUSINESS = {
    "name": "Putters Bar & Grill",
    "type": "BarOrPub",                      # deepest truthful schema.org type
    "street": "503 W Verona Ave Suite 400",
    "city": "Verona", "region": "WI", "zip": "53593", "country": "US",
    "lat": 42.9884718, "lng": -89.5416319,   # from the business's Google Maps pin
    "phone": "+16084970170",
    "email": "hurley.puttersverona@yahoo.com",
    "logo": f"{DOMAIN}/assets/logo.png",          # 1402x1122 raster
    "image": f"{DOMAIN}/assets/img/hero-crowd.jpg",
    "map": "https://www.google.com/maps/search/?api=1&query=503+W+Verona+Ave+Suite+400+Verona+WI+53593",
    "cuisine": ["American"],
    # Visible hours (contact.html). Sat-Sun show "Call for hours" -> omitted (rule 7).
    "hours": [
        {"days": ["Monday"], "opens": "16:00", "closes": "22:00"},
        {"days": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "22:00"},
    ],
    # Visible amenities (index.html copy: screens, full bar, patio, 6 TrackMan bays)
    "amenities": ["Wall-to-wall TV screens", "Full bar", "Outdoor patio",
                  "TrackMan golf simulators (6 bays)"],
    "sameAs": [],  # add GBP / social profile URLs here once confirmed (README)
}

SERVICE_RADIUS_MI = 30
RADIUS_METERS = round(SERVICE_RADIUS_MI * 1609.34)  # 48280

# Incorporated cities & villages within 30 mi of the business pin (haversine),
# nearest first. wiki=None -> title pattern "{Name},_Wisconsin".
# Brooklyn's article title verified as disambiguated (Sep 2026).
CITIES = [
    ("Verona", None, "Q1569520"), ("Fitchburg", None, "Q1570633"), ("Middleton", None, "Q1570640"),
    ("Shorewood Hills", None), ("Belleville", None, "Q2609930"), ("Oregon", None, "Q936062"),
    ("Madison", None, "Q43788"), ("Mount Horeb", None, "Q2226176"), ("Cross Plains", None, "Q2085810"),
    ("Maple Bluff", None), ("Monona", None),
    ("Brooklyn", "Brooklyn_(village),_Wisconsin", "Q2322312"),
    ("McFarland", None), ("New Glarus", None), ("Black Earth", None),
    ("Waunakee", None), ("Blue Mounds", None), ("Monticello", None),
    ("Stoughton", None), ("Barneveld", None), ("Dane", None),
    ("Cottage Grove", None), ("Mazomanie", None), ("Windsor", None, "Q8024546"),
    ("Evansville", None), ("Albany", None), ("Blanchardville", None),
    ("DeForest", None), ("Hollandale", None), ("Sun Prairie", None),
    ("Sauk City", None), ("Lodi", None), ("Prairie du Sac", None),
    ("Ridgeway", None), ("Arena", None), ("Deerfield", None),
    ("Arlington", None), ("Rockdale", None), ("Argyle", None),
    ("Edgerton", None), ("Cambridge", None), ("Brodhead", None),
    ("Marshall", None), ("Merrimac", None), ("Monroe", None),
    ("Footville", None), ("Poynette", None), ("Orfordville", None),
    ("Spring Green", None), ("Dodgeville", None),
]

# ------------------------------------------------- SERVICE AREAS (10-mi roster)
# All Wikidata Q-IDs individually verified 2026-09-08. Coordinates from
# Wikipedia/Wikidata. kind: "City" = incorporated, "Place" = unincorporated.
WISCONSIN = {"name": "Wisconsin", "qid": "Q1537",
             "wiki": "https://en.wikipedia.org/wiki/Wisconsin"}
SERVICE_AREAS = [
    # name, page file, lat, lng, qid, wikipedia title, kind, tag (about-grid label)
    ("Verona", "verona-wi.html", 42.98972, -89.53556, "Q1569520", "Verona,_Wisconsin", "City", "Our Home"),
    ("Fitchburg", "fitchburg-wi.html", 43.0117, -89.4262, "Q1570633", "Fitchburg,_Wisconsin", "City", "Just East"),
    ("Madison", "madison-wi.html", 43.0731, -89.4012, "Q43788", "Madison,_Wisconsin", "City", "10 Miles NE"),
    ("Middleton", "middleton-wi.html", 43.06028, -89.57167, "Q1570640", "Middleton,_Wisconsin", "City", "Short Drive"),
    ("Paoli", "paoli-wi.html", 42.92944, -89.52361, "Q7132120", "Paoli,_Wisconsin", "Place", "Just South"),
    ("Oregon", "oregon-wi.html", 42.90444, -89.42972, "Q936062", "Oregon,_Wisconsin", "City", "Nearby"),
    ("Mount Horeb", "mount-horeb-wi.html", 43.00639, -89.73417, "Q2226176", "Mount_Horeb,_Wisconsin", "City", "Trail West"),
    ("Cross Plains", "cross-plains-wi.html", 43.09472, -89.66111, "Q2085810", "Cross_Plains,_Wisconsin", "City", "Up North"),
    ("Belleville", "belleville-wi.html", 42.87000, -89.53806, "Q2609930", "Belleville,_Wisconsin", "City", "Sugar River"),
    ("Riley", "riley-wi.html", 43.02333, -89.62250, "Q7334167", "Riley,_Wisconsin", "Place", "On the Trail"),
    ("Mount Vernon", "mount-vernon-wi.html", 42.94694, -89.65583, "Q6924346", "Mount_Vernon,_Wisconsin", "Place", "Countryside"),
]
SERVICE_AREA_BY_FILE = {a[1]: a for a in SERVICE_AREAS}

def city_entity(area, url):
    """Rich page-scoped place entity: geo + verified Wikidata + containedInPlace."""
    name, _, lat, lng, qid, wiki, kind, _tag = area
    return {
        "@type": kind, "@id": f"{url}#city",
        "name": f"{name}, Wisconsin",
        "geo": {"@type": "GeoCoordinates", "@id": f"{url}#citygeo",
                "latitude": lat, "longitude": lng},
        "sameAs": [f"https://en.wikipedia.org/wiki/{wiki}",
                   f"https://www.wikidata.org/wiki/{qid}"],
        "containedInPlace": {"@type": "State", "@id": f"{url}#state",
                             "name": WISCONSIN["name"],
                             "sameAs": [WISCONSIN["wiki"],
                                        f"https://www.wikidata.org/wiki/{WISCONSIN['qid']}"]},
    }

COUNTIES = ["Dane", "Green", "Iowa", "Rock", "Sauk", "Columbia", "Lafayette"]

# Per-page metadata: breadcrumb trail (name, file) and WebPage subtype.
PAGES = {
    "index.html":  {"ptype": "WebPage",       "crumbs": [("Home", "index.html")]},
    "about.html":  {"ptype": "AboutPage",     "crumbs": [("Home", "index.html"), ("About Us", "about.html")]},
    "menu.html":   {"ptype": "WebPage",       "crumbs": [("Home", "index.html"), ("Food Menu", "menu.html")]},
    "specials.html": {"ptype": "WebPage",     "crumbs": [("Home", "index.html"), ("Specials & Events", "specials.html")]},
    "gallery.html": {"ptype": "CollectionPage", "crumbs": [("Home", "index.html"), ("Gallery", "gallery.html")]},
    "contact.html": {"ptype": "ContactPage",  "crumbs": [("Home", "index.html"), ("Contact & Location", "contact.html")]},
    "careers.html": {"ptype": "WebPage",      "crumbs": [("Home", "index.html"), ("Contact & Location", "contact.html"), ("Join Our Team", "careers.html")]},
    "verona-wi.html": {"ptype": "WebPage",    "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Verona, Wisconsin", "verona-wi.html")]},
    "service-areas.html": {"ptype": "CollectionPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html")]},
    "fitchburg-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Fitchburg, Wisconsin", "fitchburg-wi.html")]},
    "madison-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Madison, Wisconsin", "madison-wi.html")]},
    "middleton-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Middleton, Wisconsin", "middleton-wi.html")]},
    "paoli-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Paoli, Wisconsin", "paoli-wi.html")]},
    "oregon-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Oregon, Wisconsin", "oregon-wi.html")]},
    "mount-horeb-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Mount Horeb, Wisconsin", "mount-horeb-wi.html")]},
    "cross-plains-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Cross Plains, Wisconsin", "cross-plains-wi.html")]},
    "belleville-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Belleville, Wisconsin", "belleville-wi.html")]},
    "riley-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Riley, Wisconsin", "riley-wi.html")]},
    "mount-vernon-wi.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Service Areas", "service-areas.html"), ("Mount Vernon, Wisconsin", "mount-vernon-wi.html")]},
    "sitemap.html": {"ptype": "CollectionPage", "crumbs": [("Home", "index.html"), ("Sitemap", "sitemap.html")]},
    "privacy.html": {"ptype": "WebPage",      "crumbs": [("Home", "index.html"), ("Privacy Policy", "privacy.html")]},
    "equal-opportunity.html": {"ptype": "WebPage", "crumbs": [("Home", "index.html"), ("Equal Opportunity", "equal-opportunity.html")]},
}

def page_url(fname):
    return f"{DOMAIN}/" if fname == "index.html" else f"{DOMAIN}/{fname}"

# ---------------------------------------------------------------- helpers
def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()

def head_meta(src):
    title = clean(re.search(r"<title>(.*?)</title>", src, re.S).group(1))
    m = re.search(r'name="description" content="([^"]*)"', src)
    desc = clean(m.group(1)) if m else None
    m = re.search(r'property="og:image" content="([^"]*)"', src)
    ogimg = m.group(1) if m else None
    return title, desc, ogimg

# ---------------------------------------------------------------- area served
def area_served():
    nodes = [{
        "@type": "GeoCircle",
        "geoMidpoint": {"@type": "GeoCoordinates",
                        "latitude": BUSINESS["lat"], "longitude": BUSINESS["lng"]},
        "geoRadius": RADIUS_METERS,
        "description": f"{SERVICE_RADIUS_MI}-mile radius around Putters Bar & Grill in Verona, WI",
    }]
    for entry in CITIES:
        name, wiki, qid = (entry + (None,))[:3] if len(entry) == 2 else entry
        title = wiki or f"{name.replace(' ', '_')},_Wisconsin"
        same = [f"https://en.wikipedia.org/wiki/{title}"]
        if qid:  # Wikidata Q-IDs only when individually verified (rule 10)
            same.append(f"https://www.wikidata.org/wiki/{qid}")
        nodes.append({"@type": "City", "name": f"{name}, WI",
                      "sameAs": same if len(same) > 1 else same[0]})
    for name, lat, lng, qid, wiki in [
        ("Paoli", 42.92944, -89.52361, "Q7132120", "Paoli,_Wisconsin"),
        ("Riley", 43.02333, -89.62250, "Q7334167", "Riley,_Wisconsin"),
        ("Mount Vernon", 42.94694, -89.65583, "Q6924346", "Mount_Vernon,_Wisconsin")]:
        nodes.append({"@type": "Place", "name": f"{name}, WI",
                      "sameAs": [f"https://en.wikipedia.org/wiki/{wiki}",
                                 f"https://www.wikidata.org/wiki/{qid}"]})
    for c in COUNTIES:
        same = [f"https://en.wikipedia.org/wiki/{c}_County,_Wisconsin"]
        if c == "Dane":  # Q-ID verified 2026-09-08
            same.append("https://www.wikidata.org/wiki/Q502200")
        nodes.append({"@type": "AdministrativeArea", "name": f"{c} County, WI",
                      "sameAs": same if len(same) > 1 else same[0]})
    return nodes

# ---------------------------------------------------------------- menu parser
def parse_menu(src):
    tabs = dict(re.findall(r'data-tab="(tab-[\w-]+)">(.*?)</button>', src))
    panels = re.split(r'<div class="tab-panel[^"]*" id="(tab-[\w-]+)"', src)[1:]
    sections = []
    for tab_id, body in zip(panels[0::2], panels[1::2]):
        items = []
        # photo cards
        for h3, price, desc in re.findall(
            r'<div class="menu-card__row"><h3>(.*?)</h3>.*?menu-card__price">(.*?)</span></div>\s*<p>(.*?)</p>',
            body, re.S):
            items.append((clean(h3), clean(price), clean(desc)))
        # text list items
        for h3, price, desc in re.findall(
            r'<div class="price-row"[^>]*><h3>(.*?)</h3>.*?class="price">(.*?)</span></div>\s*<p class="price-desc">(.*?)</p>',
            body, re.S):
            items.append((clean(h3), clean(price), clean(desc)))
        menu_items = []
        for name, price, desc in items:
            mi = {"@type": "MenuItem", "name": name}
            if desc:
                mi["description"] = desc
            prices = re.findall(r"\$(\d+\.\d{2})", price)
            if len(prices) == 1:
                mi["offers"] = {"@type": "Offer", "price": prices[0], "priceCurrency": "USD"}
            elif len(prices) > 1:
                mi["offers"] = [{"@type": "Offer", "price": p, "priceCurrency": "USD"} for p in prices]
            menu_items.append(mi)
        if menu_items:
            sections.append({"@type": "MenuSection",
                             "name": clean(tabs.get(tab_id, tab_id)),
                             "hasMenuItem": menu_items})
    return {
        "@type": "Menu", "@id": f"{DOMAIN}/menu.html#menu",
        "name": "Putters Bar & Grill Food Menu",
        "inLanguage": "en-US",
        "hasMenuSection": sections,
        "mainEntityOfPage": {"@id": f"{DOMAIN}/menu.html#webpage"},
    }

# ---------------------------------------------------------------- actions
def entry_point(url):
    return {"@type": "EntryPoint", "urlTemplate": url, "inLanguage": "en-US",
            "actionPlatform": ["http://schema.org/DesktopWebPlatform",
                               "http://schema.org/MobileWebPlatform"]}

def field(name):
    return {"@type": "PropertyValueSpecification", "valueName": name, "valueRequired": True}

def potential_actions():
    contact = entry_point(f"{DOMAIN}/contact.html#contactForm")
    careers = entry_point(f"{DOMAIN}/careers.html#careersForm")
    return [
        # contact.html form: name*, email*, message* (type select optional)
        {"@type": "AskAction", "name": "Contact Putters Bar & Grill", "target": contact,
         "name-input": field("name"), "email-input": field("email"), "message-input": field("message")},
        # same form, "Table Booking" option
        {"@type": "ReserveAction", "name": "Book a Table", "target": contact,
         "name-input": field("name"), "email-input": field("email"), "message-input": field("message")},
        # careers.html form: name*, email*, message* (phone, role optional)
        {"@type": "ApplyAction", "name": "Apply to Join Our Team", "target": careers,
         "name-input": field("name"), "email-input": field("email"), "message-input": field("message")},
        {"@type": "CommunicateAction", "name": "Call Putters Bar & Grill",
         "target": entry_point(f"tel:{BUSINESS['phone']}")},
        {"@type": "CommunicateAction", "name": "Email Putters Bar & Grill",
         "target": entry_point(f"mailto:{BUSINESS['email']}")},
    ]

# ---------------------------------------------------------------- core nodes
def menu_price_range():
    """priceRange derived from prices published on menu.html — never asserted."""
    prices = [float(p) for p in re.findall(r"\$(\d+\.\d{2})",
              (ROOT / "menu.html").read_text(encoding="utf-8"))]
    return f"${min(prices):.2f}-${max(prices):.2f}" if prices else None

def business_node(on_menu_page):
    price_range = menu_price_range()
    b = {
        "@type": BUSINESS["type"], "@id": f"{DOMAIN}/#business",
        "name": BUSINESS["name"], "url": f"{DOMAIN}/",
        "image": BUSINESS["image"],
        "logo": {"@type": "ImageObject", "url": BUSINESS["logo"], "width": 1402, "height": 1122},
        "address": {"@type": "PostalAddress", "streetAddress": BUSINESS["street"],
                    "addressLocality": BUSINESS["city"], "addressRegion": BUSINESS["region"],
                    "postalCode": BUSINESS["zip"], "addressCountry": BUSINESS["country"]},
        "geo": {"@type": "GeoCoordinates", "latitude": BUSINESS["lat"], "longitude": BUSINESS["lng"]},
        "hasMap": BUSINESS["map"],
        "telephone": BUSINESS["phone"], "email": BUSINESS["email"],
        "servesCuisine": BUSINESS["cuisine"],
        **({"priceRange": price_range} if price_range else {}),
        "acceptsReservations": f"{DOMAIN}/contact.html#contactForm",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"],
             "opens": h["opens"], "closes": h["closes"]} for h in BUSINESS["hours"]],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": a, "value": True}
                           for a in BUSINESS["amenities"]],
        "areaServed": area_served(),
        "hasMenu": {"@id": f"{DOMAIN}/menu.html#menu"} if on_menu_page else f"{DOMAIN}/menu.html",
        "potentialAction": potential_actions(),
    }
    if BUSINESS["sameAs"]:
        b["sameAs"] = BUSINESS["sameAs"]
    return b

def website_node():
    return {"@type": "WebSite", "@id": f"{DOMAIN}/#website",
            "name": BUSINESS["name"], "url": f"{DOMAIN}/",
            "publisher": {"@id": f"{DOMAIN}/#business"}, "inLanguage": "en-US"}

def breadcrumb_node(fname, crumbs):
    return {"@type": "BreadcrumbList", "@id": f"{page_url(fname)}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n,
                 "item": page_url(f)} for i, (n, f) in enumerate(crumbs)]}

def webpage_node(fname, meta, ptype, main_entity=None, about=None):
    title, desc, ogimg = meta
    url = page_url(fname)
    wp = {"@type": ptype, "@id": f"{url}#webpage", "url": url, "name": title,
          "isPartOf": {"@id": f"{DOMAIN}/#website"},
          "about": about or {"@id": f"{DOMAIN}/#business"},
          "breadcrumb": {"@id": f"{url}#breadcrumb"}, "inLanguage": "en-US"}
    if desc:
        wp["description"] = desc
    pub, mod = git_dates(fname)
    if pub:
        wp["datePublished"] = pub
    if mod:
        wp["dateModified"] = mod
    if ogimg:
        wp["primaryImageOfPage"] = {"@type": "ImageObject", "url": ogimg}
    if main_entity:
        wp["mainEntity"] = main_entity
    return wp

# ---------------------------------------------------------------- build graph
def build_graph(fname, src):
    meta = head_meta(src)
    cfg = PAGES[fname]
    on_menu = fname == "menu.html"
    nodes = [website_node(), business_node(on_menu), breadcrumb_node(fname, cfg["crumbs"])]
    if on_menu:
        menu = parse_menu(src)
        nodes.append(webpage_node(fname, meta, cfg["ptype"],
                                  main_entity={"@id": menu["@id"]}))
        nodes.append(menu)
    elif fname in SERVICE_AREA_BY_FILE:
        city = city_entity(SERVICE_AREA_BY_FILE[fname], page_url(fname))
        ref = {"@id": city["@id"]}
        nodes.append(webpage_node(fname, meta, cfg["ptype"], main_entity=ref, about=ref))
        nodes.append(city)
    else:
        nodes.append(webpage_node(fname, meta, cfg["ptype"]))
    return {"@context": "https://schema.org", "@graph": nodes}

# ---------------------------------------------------------------- integrity
def walk_ids(obj, defined, referenced):
    if isinstance(obj, dict):
        if set(obj.keys()) == {"@id"}:
            referenced.add(obj["@id"])
        elif "@id" in obj:
            defined.add(obj["@id"])
        for v in obj.values():
            walk_ids(v, defined, referenced)
    elif isinstance(obj, list):
        for v in obj:
            walk_ids(v, defined, referenced)

def integrity_check(fname, graph, src):
    defined, referenced = set(), set()
    walk_ids(graph, defined, referenced)
    dangling = referenced - defined
    assert not dangling, f"{fname}: dangling @id(s): {dangling}"
    json.loads(json.dumps(graph))  # round-trip parse
    # anchors used by actions must exist somewhere in the site
    for anchor, target in [("contactForm", "contact.html"), ("careersForm", "careers.html")]:
        tsrc = (ROOT / target).read_text(encoding="utf-8")
        assert f'id="{anchor}"' in tsrc, f"{target}: missing #{anchor} anchor"
    return len(defined), len(json.dumps(graph))

# ---------------------------------------------------------------- inject
MARK_A = "<!-- BEGIN JSON-LD SCHEMA (generated by tools/schema.py - do not edit by hand) -->"
MARK_B = "<!-- END JSON-LD SCHEMA -->"

def inject(fname, src, graph):
    payload = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    block = f'{MARK_A}\n  <script type="application/ld+json">{payload}</script>\n  {MARK_B}'
    if MARK_A in src:
        src = re.sub(re.escape(MARK_A) + r".*?" + re.escape(MARK_B), block, src, flags=re.S)
    else:
        src = src.replace("</head>", f"  {block}\n</head>", 1)
    (ROOT / fname).write_text(src, encoding="utf-8")

# ---------------------------------------------------------------- main
def main():
    check_only = "--check" in sys.argv
    for fname in PAGES:
        src = (ROOT / fname).read_text(encoding="utf-8")
        graph = build_graph(fname, src)
        n_ids, size = integrity_check(fname, graph, src)
        if not check_only:
            inject(fname, src, graph)
        print(f"  {'OK  ' if check_only else 'DONE'} {fname:26} {n_ids} @ids defined, {size/1024:.1f} KB")
    print("integrity: all @id references resolve, JSON parses, form anchors exist")

if __name__ == "__main__":
    main()
