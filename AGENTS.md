# AGENTS.md — Putters Bar & Grill website

Context for AI agents (and humans) working on this repo. Read this before
editing anything.

## What this is
Static marketing site for **Putters Bar & Grill** (formerly The Bogey
Factory), 503 W Verona Ave Suite 400, Verona, WI 53593 · (608) 497-0170 ·
hurley.puttersverona@yahoo.com. Sports bar + 6 TrackMan golf simulator bays.
Live at **https://puttersverona.com** (Vercel auto-deploys `main`; also
mirrored on GitHub Pages). Hand-written HTML/CSS/JS — no framework, no
build step, and keep it that way.

## Design system — "Champion's Reserve" (Stadium Prime Green)
- Dark theme. Tokens live in `:root` in `css/style.css`:
  `--surface` #0d0d0d family, `--on-surface` #e4e4e2, accent
  `--primary` #7fda8b (Action Green) with `--on-primary` #003913.
  Always use the CSS variables, never raw hex in markup.
- Fonts: Anybody (display), Hanken Grotesk (body), JetBrains Mono (stats/
  tickers). Headings use an `<em>` inside for the green italic accent word.
- Components: `.chip`, `.btn--primary/.btn--outline`, `.menu-card`,
  `.price-row` + `.dots` leader, `.tab-btn`/`.tab-panel`, `.section__head`
  with `.kicker`. Match existing patterns before inventing new ones.
- Respect `prefers-reduced-motion`; keep the mobile nav working.

## File map
- `index.html` home · `about.html` (has Service Area section) ·
  `menu.html` ("The Playbook", 7 tabbed sections) · `specials.html` ·
  `gallery.html` (tabs: Plate / Interior / Exterior, lightbox) ·
  `contact.html` (form + map + hours) · `careers.html` (application form) ·
  `verona-wi.html` (local-SEO city guide) · legal: `sitemap.html`,
  `privacy.html`, `equal-opportunity.html`.
- `tools/schema.py` — JSON-LD generator (see below).
- `google677f148e16a35022.html` — Search Console verification. Never touch.

## Structured data (important)
Every page carries a generated JSON-LD `@graph` between
`BEGIN/END JSON-LD SCHEMA` markers. **Never hand-edit those blocks.**
After editing any page (especially the menu), run:

    python3 tools/schema.py

It re-parses `menu.html` for Menu items/prices and priceRange, pulls
`datePublished`/`dateModified` from git history, and runs an @id
integrity check. Policy of what is deliberately NOT marked up (events,
job postings, reviews, weekend hours) is in `README.md` — read it before
adding schema types.

Visible breadcrumbs on subpages mirror the `PAGES` trails defined in
`tools/schema.py`. If you add a page: add it to `PAGES`, add a canonical
tag + OG tags + sitemap.xml entry, add a visible breadcrumb nav, and
re-run the generator.

## Forms
Both forms POST to FormSubmit (`formsubmit.co/ajax/<email>`), handled by
`wireForm()` in `js/main.js` with inline `.form-status` feedback and a
`_honey` honeypot. Required fields are name/email/message — these must
stay 1:1 with the `PropertyValueSpecification` inputs in the schema's
potentialActions. If the destination email ever changes, update:
form `action` attributes, the fetch URL in `js/main.js`, `BUSINESS`
in `tools/schema.py`, and the mailto links site-wide.

## Content ground rules
- Address always includes "Suite 400". Phone format (608) 497-0170.
- The rebrand matters: never surface "Bogey Factory" branding to guests
  (it exists only in historical notes and one gallery editorial decision).
- `verona-wi.html` facts were research-verified — don't "refresh" them
  from memory; verify before changing.
- Don't add Wikidata Q-IDs or `sameAs` profile URLs without verifying
  each one (see README schema section).

## Service-area city pages
Ten city guides ({slug}-wi.html) built by `tools/build_city_pages.py` (one-shot;
content lives in that script's per-city dicts — every paragraph is city-specific
and must stay that way: no sentence should survive swapping the city name).
Hub: service-areas.html. Hierarchy: Home / Service Areas / {City}. Each page:
unique title/desc/canonical/OG, stat cards, 2 researched paragraphs, game-day
route, rotating amenity chips + CTA, Nearby-communities links, and a generated
@graph with a page-scoped City/Place entity (geo + Wikipedia + Wikidata).

## Known open items (as of Sep 2026)
- Weekend hours: contact.html says "Call for hours"; schema omits Sat–Sun.
  Weekday hours trace to the old Bogey Factory listing — unverified.
- `specials.html` schedule and reviews are **sample content** — that's why
  no Event schema exists.
- `BUSINESS["sameAs"]` is empty pending the Google Business Profile URL.
- FormSubmit requires one-time activation: the first submission emails an
  activation link to the Yahoo address; the owner must click it.

## Workflow
Commit as `MMG001 <MMG001@users.noreply.github.com>`. Push to `main`
deploys automatically. Never commit tokens; scrub them from any logged
output (`sed "s/${GH_TOKEN}/***/g"`).
