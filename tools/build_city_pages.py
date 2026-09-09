#!/usr/bin/env python3
"""One-shot builder for the 10 service-area city pages.
Every paragraph below is hand-written per city from verified research
(Wikipedia/Wikidata/municipal sources, Sep 2026) — nothing survives a
city-name swap. Facts: populations are 2020 census unless noted."""
import html, re

PIN = '<svg class="svc-row__pin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'

C = {}  # slug -> content dict

C["fitchburg"] = dict(
 name="Fitchburg", wiki="Fitchburg,_Wisconsin", tag="Just East",
 title="Fitchburg, WI Sports Bar Nearby | Putters Bar &amp; Grill — Verona",
 desc="Putters Bar &amp; Grill is Fitchburg's next-door sports bar — 10 minutes down McKee Road in downtown Verona. Screens, scratch kitchen, and 6 TrackMan golf bays.",
 h1='Fitchburg, meet your <em>overtime bar</em>',
 lede="Ten minutes of McKee Road is all that separates Fitchburg's west side from the best seat for the game.",
 stats=[("&#127963;","County","Dane County"),("&#128101;","Population","25,000+ residents"),
        ("&#128205;","From Putters","About 6 miles east"),("&#128220;","Incorporated","1983 — by court fight")],
 about_h='About Fitchburg, <em>Wisconsin</em>',
 about=["Fitchburg is Verona's next-door city to the east and one of the youngest cities in the state by charter — it incorporated in 1983 only after taking its fight against Madison's annexations all the way to the Wisconsin Supreme Court, and winning. Its 35 square miles run from biotech and tech-campus corridors in the north to open farmland in the south, and it's served by three school districts — including the Verona Area School District, which covers its western neighborhoods. Functionally, a good slice of Fitchburg already lives on our home turf.",
        "It's also the Madison area's most deliberately bike-first city, recognized by the League of American Bicyclists since 2012, with Quarry Ridge's wooded mountain-bike trails tying into both the Capital City and Military Ridge State Trails. Point your wheels west on Military Ridge and the old rail grade all but delivers you to downtown Verona."],
 game_h='Game day <em>from Fitchburg</em>',
 game="McKee Road (County PD) runs straight off Fitchburg's west side into Verona — one road, about ten minutes, no Beltline involved. Badger Saturdays, Packers Sundays, or a post-work Trivia Tuesday out of the tech corridor: you'll beat the Madison crowds without ever merging.",
 chips=["6 TrackMan golf bays","Wall-to-wall screens","Happy hour M&ndash;F 3&ndash;6"],
 tie="When Wisconsin weather cancels your tee time, six TrackMan bays with 300+ courses don't care what it's doing outside.",
 cta=("View Specials &amp; Events","specials.html"),
 nearby=["madison","oregon","verona"], explore=[("The full menu","menu.html"),("Photo gallery","gallery.html")])

C["madison"] = dict(
 name="Madison", wiki="Madison,_Wisconsin", tag="10 Miles NE",
 title="Madison, WI Area Sports Bar | Putters Bar &amp; Grill — Verona",
 desc="Skip the Camp Randall crush — Putters Bar &amp; Grill is 10 minutes from Madison down Verona Road (US 18/151). Free parking, every game on, TrackMan golf sims.",
 h1="Madison's <em>escape hatch</em> on game day",
 lede="Ten minutes down Verona Road: the parking is free, the screens are everywhere, and nobody is towing your car off the isthmus.",
 stats=[("&#127963;","County","Dane County"),("&#128101;","Population","Roughly 270,000"),
        ("&#128205;","From Putters","About 9 miles NE"),("&#127941;","Claim to fame","State capital &amp; the UW")],
 about_h='About Madison, <em>Wisconsin</em>',
 about=["Madison needs no introduction: Wisconsin's capital and second-largest city, home of the University of Wisconsin and roughly 270,000 people famously wedged onto an isthmus between two lakes. What it cannot offer on a Badger Saturday is an easy seat — Camp Randall pulls more than 75,000 people into the neighborhood and takes most of the parking with it.",
        "Verona Road is the pressure valve. US 18/151 runs from the Beltline straight to our corner of downtown Verona, which is why so many west-side Madisonians quietly treat Putters as their neighborhood bar that happens to sit one town over — same game, shorter line, actual parking."],
 game_h='Game day <em>from Madison</em>',
 game="From the Beltline, US 18/151 southwest is about ten minutes. Watch the Badgers on a wall of screens without paying stadium-district prices — or book a TrackMan bay in January, when the lakes are frozen and your golf swing shouldn't have to be.",
 chips=["Wall-to-wall screens","Full bar","6 TrackMan golf bays"],
 tie="Every Badgers, Packers, Bucks, and Brewers broadcast, all at once — the scoreboard wall doesn't make you choose.",
 cta=("Book a Table","contact.html"),
 nearby=["fitchburg","middleton","verona"], explore=[("The full menu","menu.html"),("Specials &amp; events","specials.html")])

C["middleton"] = dict(
 name="Middleton", wiki="Middleton,_Wisconsin", tag="Short Drive",
 title="Middleton, WI Area Sports Bar | Putters Bar &amp; Grill — Verona",
 desc="From the Good Neighbor City to Verona in 15 minutes on Highway M — Putters Bar &amp; Grill: patio summers, TrackMan winters, and every game on the wall.",
 h1="The Good Neighbor City's <em>good-time neighbor</em>",
 lede="Highway M south skips Madison entirely and lands you at our door in about fifteen minutes.",
 stats=[("&#127963;","County","Dane County"),("&#128101;","Population","21,827 (2020)"),
        ("&#128205;","From Putters","About 6 miles north"),("&#128220;","A city since","1963 — once 'Peatville'")],
 about_h='About Middleton, <em>Wisconsin</em>',
 about=["Middleton wears its motto — \"The Good Neighbor City\" — honestly. Consistently ranked among the best places to live in Wisconsin, its 21,827 residents (2020) share a downtown that grew from a rail depot in a settlement once called Peatville, for the peat cut from its soils. It has been a city since 1963 and Madison's polished northwestern shoulder ever since.",
        "Between Middleton and Verona runs some of Dane County's best driving: Highway M and the county roads thread the Town of Middleton's farm hills — the same terrain the Ice Age National Scenic Trail follows on its way south past Verona. The commute to the game is, frankly, part of the show."],
 game_h='Game day <em>from Middleton</em>',
 game="Take Highway M south along the county's western hills — no Beltline, no downtown — and you're in Verona in about fifteen minutes. Middleton crews own our patio all summer and migrate to the simulator bays the week the snow flies.",
 chips=["Outdoor patio","6 TrackMan golf bays","Scratch kitchen"],
 tie="Patio season and simulator season split the year about evenly here — there is no off-season.",
 cta=("View the Menu","menu.html"),
 nearby=["madison","cross-plains","verona"], explore=[("Specials &amp; events","specials.html"),("Photo gallery","gallery.html")])

C["paoli"] = dict(
 name="Paoli", wiki="Paoli,_Wisconsin", tag="Just South",
 title="Paoli, WI — Sports Bar 4 Miles North | Putters Bar &amp; Grill",
 desc="Four miles up County PB from the Paoli mills: Putters Bar &amp; Grill in downtown Verona. The natural last stop after a Sugar River gallery afternoon or bike loop.",
 h1="Four miles from the mill: <em>Paoli's late innings</em>",
 lede="County PB north is the shortest trip on our service-area list — the galleries close at five, the game tips at six, and the math works out.",
 stats=[("&#127963;","Township","Town of Montrose, Dane Co."),("&#127960;","Community","Historic unincorporated hamlet"),
        ("&#128205;","From Putters","About 4 miles south"),("&#128220;","Roots","Settled 1846 by Peter Matts")],
 about_h='About Paoli, <em>Wisconsin</em>',
 about=["Paoli may be the most charming four miles in Dane County: an 1840s mill hamlet on the Sugar River, founded after Peter Matts bought the land in 1846 and named it for Paoli, Pennsylvania. The historic Paoli Mills — on the National Register of Historic Places — now anchor a bend-in-the-river cluster of art galleries, food shops, and weekend crowds refueling at the bridge.",
        "The Sugar River rolls south out of Paoli toward Belleville; County PB rolls north to Verona. Cyclists work both directions all summer, which is why so many Paoli loops officially end — or unofficially pause — on our patio."],
 game_h='Game day <em>from Paoli</em>',
 game="County PB north, four miles, one stop sign's worth of effort. It's close enough that Paoli's gallery crowd and its spandex crowd both count as regulars — one orders the fish fry, the other orders everything.",
 chips=["Outdoor patio","Full bar","Happy hour M&ndash;F 3&ndash;6"],
 tie="Bike racks out front; recovery carbs, scratch-made, inside.",
 cta=("View Specials &amp; Events","specials.html"),
 nearby=["belleville","mount-vernon","oregon"], explore=[("The full menu","menu.html"),("Verona city guide","verona-wi.html")])

C["oregon"] = dict(
 name="Oregon", wiki="Oregon,_Wisconsin", tag="Nearby",
 title="Oregon, WI Sports Bar Nearby | Putters Bar &amp; Grill — Verona",
 desc="Oregon to Verona is 15 minutes across the countryside. Putters Bar &amp; Grill: every Panthers rival and Badgers broadcast on the wall, wings tossed to order.",
 h1="From Rome Corners to <em>our corner</em>",
 lede="Oregon started at a crossroads in 1841 — we're just the crossroads fifteen minutes northwest with a scoreboard wall.",
 stats=[("&#127963;","County","Dane County"),("&#128101;","Population","11,179 (2020)"),
        ("&#128205;","From Putters","About 8 miles SE"),("&#128220;","Incorporated","1881 — b. 'Rome Corners' 1841")],
 about_h='About Oregon, <em>Wisconsin</em>',
 about=["Oregon began at Rome Corners, settled in 1841 where the old Lead Road from Mineral Point crossed the Madison–Janesville mail route — and it kept the crossroads habit: US 14 and WIS 138 meet at the village's corner today. The railroad renamed the place Oregon on its 1864 maps, the village incorporated in 1881, and 11,179 people (2020) now call it home at the southern edge of the Madison area.",
        "Oregon and Verona anchor southwest Dane County's school-rivalry belt, eight miles of farmland apart — close enough that plenty of Friday nights split a family between Panther and Wildcat bleachers before everyone reconvenes over a basket of wings."],
 game_h='Game day <em>from Oregon</em>',
 game="County roads northwest through the fields, about fifteen minutes, tractor traffic permitting. After Panthers football or a youth-league Saturday, the scoreboard wall keeps every remaining game in one field of view.",
 chips=["Wall-to-wall screens","Scratch kitchen","Full bar"],
 tie="Ten homemade wing sauces, from Garlic Parmesan to Nashville Hot — rivalries settle faster over a shared basket.",
 cta=("View the Menu","menu.html"),
 nearby=["fitchburg","paoli","belleville"], explore=[("Specials &amp; events","specials.html"),("Photo gallery","gallery.html")])

C["mount-horeb"] = dict(
 name="Mount Horeb", wiki="Mount_Horeb,_Wisconsin", tag="Trail West",
 title="Mount Horeb, WI — Sports Bar on the Trail East | Putters Bar &amp; Grill",
 desc="From the Troll Capital, take US 18/151 or the Military Ridge Trail east to Putters Bar &amp; Grill in Verona — TrackMan golf bays, patio, and every game on.",
 h1="Trolls to the west, <em>birdies to the east</em>",
 lede="The Military Ridge Trail ties the Troll Capital to our block of Verona — about ten miles of old rail grade, downhill-trending in the direction of cold taps.",
 stats=[("&#127963;","County","Dane County"),("&#128101;","Population","7,754 (2020)"),
        ("&#128205;","From Putters","About 10 miles west"),("&#129482;","Claim to fame","Troll Capital of the World")],
 about_h='About Mount Horeb, <em>Wisconsin</em>',
 about=["Mount Horeb is the Troll Capital of the World — the carved trolls along its downtown \"Trollway\" honor a Norwegian heritage that has shaped the village since the first immigrants arrived in the 1870s. Its 7,754 residents (2020) live at the doorstep of the Driftless Area, with Blue Mound State Park over one shoulder and the National Mustard Museum, improbably and gloriously, on Main Street.",
        "US 151 carries Mount Horeb's commuters toward the Madison area, but the better connection to Verona is older: the Military Ridge State Trail follows the historic rail grade between the two downtowns, and riders have been known to earn their cheese curds twice — once in each direction."],
 game_h='Game day <em>from Mount Horeb</em>',
 game="US 18/151 east is the fast way — call it fifteen minutes. The trail is the fun way. Either route, Vikings of the Norwegian variety are always welcome; Vikings fans, we'll allow it on non-Packers days.",
 chips=["6 TrackMan golf bays","Outdoor patio","Happy hour M&ndash;F 3&ndash;6"],
 tie="Blue Mound is real golf country in July — our TrackMan bays keep the season alive the other nine months.",
 cta=("Book a Table","contact.html"),
 nearby=["mount-vernon","riley","cross-plains"], explore=[("The full menu","menu.html"),("Specials &amp; events","specials.html")])

C["cross-plains"] = dict(
 name="Cross Plains", wiki="Cross_Plains,_Wisconsin", tag="Up North",
 title="Cross Plains, WI Area Sports Bar | Putters Bar &amp; Grill — Verona",
 desc="Twenty minutes from Black Earth Creek to Putters Bar &amp; Grill in Verona — County P through the Driftless hills to a scratch kitchen and every game on the wall.",
 h1="Famous for friendliness, <em>fluent in game day</em>",
 lede="County P south through Pine Bluff's ridges might be the prettiest game-day commute in Dane County — twenty minutes, especially worth it in October.",
 stats=[("&#127963;","County","Dane County"),("&#128101;","Population","4,104 (2020)"),
        ("&#128205;","From Putters","About 10 miles north"),("&#127907;","Claim to fame","Black Earth Creek trout water")],
 about_h='About Cross Plains, <em>Wisconsin</em>',
 about=["Cross Plains calls itself \"Famous for Friendliness\" and backs the claim with geography: the village of 4,104 (2020) sits where Black Earth Creek — one of Wisconsin's storied trout streams — cuts between bluffs at the gateway to the Driftless Area, with the Ice Age National Scenic Trail threading the hills above town. Incorporated in 1920, it was assembled from three earlier settlements: Cross Plains, Foxville, and Christina.",
        "Anglers' hours and bar hours were made for each other. Creek at first light, hatch by noon — and by the time the waders are drying on the tailgate, the afternoon slate is already up on our wall in Verona."],
 game_h='Game day <em>from Cross Plains</em>',
 game="County P winds south through Pine Bluff and the ridge farms to Verona in about twenty minutes. US 14 to Madison exists, sure — but nobody ever pulled over on the Beltline to watch the leaves turn.",
 chips=["Scratch kitchen","Wall-to-wall screens","Full bar"],
 tie="Catch-and-release on the creek pairs correctly with catch-and-keep in our kitchen — the Friday fish fry is the lawful exception.",
 cta=("View the Menu","menu.html"),
 nearby=["middleton","riley","mount-horeb"], explore=[("Specials &amp; events","specials.html"),("Verona city guide","verona-wi.html")])

C["belleville"] = dict(
 name="Belleville", wiki="Belleville,_Wisconsin", tag="Sugar River",
 title="Belleville, WI Sports Bar Nearby | Putters Bar &amp; Grill — Verona",
 desc="Highway 69 north from Belleville along the Sugar River to Putters Bar &amp; Grill in Verona — 15 minutes to the fish fry, the scoreboard wall, and the golf sims.",
 h1="UFO sightings optional, <em>game sightings guaranteed</em>",
 lede="Highway 69 follows the Sugar River valley from Belleville to our side of Verona in about fifteen minutes — keep an eye on the sky on the way.",
 stats=[("&#127963;","Counties","Dane &amp; Green (it straddles both)"),("&#128101;","Population","2,491 (2020)"),
        ("&#128205;","From Putters","About 9 miles south"),("&#128302;","Claim to fame","Wisconsin's UFO Capital")],
 about_h='About Belleville, <em>Wisconsin</em>',
 about=["Belleville straddles the Dane–Green county line where John Frederick dammed the Sugar River in the 1840s to power his sawmill and grist mill. Its 2,491 residents (2020) share the village with Lake Belle View at the center of town, the National Register-listed Library Park and its 1894 village hall — and the state's best-cultivated UFO lore, a reputation as Wisconsin's UFO Capital that the village cheerfully leans into.",
        "The Badger State Trail runs through Belleville on the old railbed, and Highway 69 stitches the village to Paoli and on toward Verona along the river valley — a corridor people have been traveling for a good meal since the mills were grinding."],
 game_h='Game day <em>from Belleville</em>',
 game="Highway 69 north to County PB, river for company most of the way, about fifteen minutes. After a lap of Lake Belle View or a trail ride up the old railbed, the Friday fish fry is the traditional landing.",
 chips=["Full bar","Scratch kitchen","Wall-to-wall screens"],
 tie="We can't promise a sighting on the drive up — we can promise every game, all at once, on the wall.",
 cta=("View Specials &amp; Events","specials.html"),
 nearby=["paoli","oregon","verona"], explore=[("The full menu","menu.html"),("Photo gallery","gallery.html")])

C["riley"] = dict(
 name="Riley", wiki="Riley,_Wisconsin", tag="On the Trail",
 title="Riley, WI — Military Ridge Trail Sports Bar | Putters Bar &amp; Grill",
 desc="Riley to Putters Bar &amp; Grill is five flat miles on the Military Ridge Trail into downtown Verona. Bike racks out front, recovery carbs inside.",
 h1="A trail stop with <em>a nineteenth hole</em>",
 lede="Five flat miles of crushed limestone separate Riley from our door — close enough to ride in for the first quarter and coast home before dark.",
 stats=[("&#127963;","Township","Town of Springdale, Dane Co."),("&#127960;","Community","Rail-stop crossroads"),
        ("&#128205;","From Putters","About 5 miles west"),("&#128220;","Roots","Post office 1882&ndash;1940")],
 about_h='About Riley, <em>Wisconsin</em>',
 about=["Riley is barely a dot on the Dane County map — a Town of Springdale crossroads named for the Riley brothers, who owned the land when the railroad came through, with a post office that served the settlement from 1882 to 1940. But every Military Ridge Trail rider knows it: Riley is the classic first waypoint on the grade west out of Verona.",
        "The trail between Riley and our end of town runs through Sugar River headwaters country — five miles so flat and fast that Riley functionally counts as a Verona neighborhood with better birdwatching."],
 game_h='Game day <em>from Riley</em>',
 game="Riley Road if you're driving; the trail if you're doing it right. Either way it's a five-mile trip — rack the bike out front and we'll handle the recovery carbs and the second half.",
 chips=["Outdoor patio","Happy hour M&ndash;F 3&ndash;6","Scratch kitchen"],
 tie="Trail miles convert to curd calories at a generous exchange rate here.",
 cta=("View the Menu","menu.html"),
 nearby=["mount-vernon","cross-plains","mount-horeb"], explore=[("Specials &amp; events","specials.html"),("Verona city guide","verona-wi.html")])

C["mount-vernon"] = dict(
 name="Mount Vernon", wiki="Mount_Vernon,_Wisconsin", tag="Countryside",
 title="Mount Vernon, WI — Sports Bar 6 Miles East | Putters Bar &amp; Grill",
 desc="From the Big Spring valley, County G climbs to US 18/151 and Putters Bar &amp; Grill in Verona — ten minutes to hot plates, cold taps, and every game.",
 h1="Spring-water valley, <em>cold taps six miles on</em>",
 lede="County G climbs out of the Mount Vernon Creek valley to US 18/151 — call it ten minutes from the Big Spring to our scoreboard wall.",
 stats=[("&#127963;","Township","Town of Springdale, Dane Co."),("&#127960;","Community","Historic mill hamlet"),
        ("&#128205;","From Putters","About 6 miles SW"),("&#128220;","Roots","Britts family mill, 1847")],
 about_h='About Mount Vernon, <em>Wisconsin</em>',
 about=["Mount Vernon grew up around the Big Spring on Mount Vernon Creek, a branch of the Sugar River, where the Britts family — Virginians who named the settlement for Mount Vernon back home — built a mill in 1847. A grist mill followed in 1858, grinding for farmers hauling freight on the old lead roads; today the spring anchors Donald Park, one of Dane County's quietest and best.",
        "The valley between Mount Vernon and Verona is textbook Driftless: trout water, ridge roads, red barns. It's the kind of six miles that makes the drive to dinner feel like part of the evening."],
 game_h='Game day <em>from Mount Vernon</em>',
 game="County G to US 18/151, about ten minutes. After a Donald Park hike or an evening on the creek, a hot plate from the scratch kitchen and the full scoreboard wall are the correct next stop.",
 chips=["Scratch kitchen","Full bar","Outdoor patio"],
 tie="Springdale township raised on spring water deserves a properly cold tap line — we keep ours honest.",
 cta=("Book a Table","contact.html"),
 nearby=["riley","paoli","mount-horeb"], explore=[("The full menu","menu.html"),("Photo gallery","gallery.html")])

# ---------------------------------------------------------------- build
shell = open("about.html").read()
header = shell[shell.index("<body>"):shell.index('<main id="main">')].replace(
    '<a href="about.html" class="is-active">', '<a href="about.html">')
footer = shell[shell.index("</main>"):]

SLUG2FILE = {s: f"{s}-wi.html" for s in C}
SLUG2FILE["verona"] = "verona-wi.html"
NAMES = {s: c["name"] for s, c in C.items()}; NAMES["verona"] = "Verona"

for slug, c in C.items():
    fname = SLUG2FILE[slug]
    url = f"https://puttersverona.com/{fname}"
    stats = "\n".join(
        f'          <article class="card"><span class="card__icon">{i}</span><h3>{t}</h3><p>{v}</p></article>'
        for i, t, v in c["stats"])
    chips = " ".join(f'<span class="chip">{ch}</span>' for ch in c["chips"])
    nearby = "\n".join(
        f'          <a class="svc-row" href="{SLUG2FILE[n]}">{PIN}<h3>{NAMES[n]}</h3><span class="svc-tag">See the guide <span aria-hidden="true">&rarr;</span></span></a>'
        for n in c["nearby"])
    explore = " &middot; ".join(f'<a href="{h}">{t}</a>' for t, h in c["explore"])
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c["title"]}</title>
  <meta name="description" content="{c["desc"]}">
  <link rel="icon" type="image/png" href="assets/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anybody:ital,wght@0,700;0,800;1,800&family=Hanken+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Putters Bar &amp; Grill">
  <meta property="og:title" content="{c["title"]}">
  <meta property="og:description" content="{c["desc"]}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://puttersverona.com/assets/img/hero-crowd.jpg">
  <meta name="twitter:card" content="summary_large_image">
</head>
{header}<main id="main">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><a href="index.html">Home</a> <span class="breadcrumbs__sep">/</span> <a href="service-areas.html">Service Areas</a> <span class="breadcrumbs__sep">/</span> <span aria-current="page">{c["name"]}, Wisconsin</span></div></nav>

    <section class="section">
      <div class="container">
        <div class="section__head" style="text-align:center; margin-inline:auto;">
          <span class="kicker">Serving {c["name"]}, WI</span>
          <h1>{c["h1"]}</h1>
          <p class="tab-panel__intro" style="margin-inline:auto;">{c["lede"]}</p>
        </div>
        <div class="cards-3" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));">
{stats}
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0;">
      <div class="container">
        <div class="section__head"><span class="kicker">The Neighborhood</span><h2>{c["about_h"]}</h2></div>
        <p>{c["about"][0]}</p>
        <p>{c["about"][1]}</p>
        <p><a href="https://en.wikipedia.org/wiki/{c["wiki"]}" target="_blank" rel="noopener">Read more about {c["name"]} on Wikipedia &rarr;</a></p>
      </div>
    </section>

    <section class="section" style="padding-top:0;">
      <div class="container">
        <div class="section__head"><span class="kicker">The Trip</span><h2>{c["game_h"]}</h2></div>
        <p>{c["game"]}</p>
        <p style="margin-top:16px;">{chips}</p>
        <p>{c["tie"]}</p>
        <div class="hero-actions" style="margin-top:24px;">
          <a class="btn btn--primary" href="{c["cta"][1]}">{c["cta"][0]}</a>
          <a class="btn btn--outline" href="https://www.google.com/maps/dir/?api=1&amp;destination=Putters+Bar+%26+Grill%2C+503+W+Verona+Ave+Suite+400%2C+Verona%2C+WI+53593" target="_blank" rel="noopener">Get Directions &#128205;</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0;">
      <div class="container">
        <div class="section__head"><span class="kicker">Keep Exploring</span><h2>Nearby <em>communities</em></h2></div>
        <div class="svc-grid">
{nearby}
        </div>
        <p style="margin-top:24px;">More from Putters: {explore} &middot; <a href="service-areas.html">All service areas</a></p>
      </div>
    </section>
  ''' + footer
    open(fname, "w").write(page)
    print("built", fname)

# --- hub: turn the ten rows into links
hub = open("service-areas.html").read()
hub = hub.replace('<a href="about.html" class="is-active">', '<a href="about.html">')
for slug, c in C.items():
    dead = f'<div class="svc-row">{PIN}<h3>{c["name"]}</h3><span class="svc-tag">{c["tag"]}</span></div>'
    live = f'<a class="svc-row" href="{SLUG2FILE[slug]}">{PIN}<h3>{c["name"]}</h3><span class="svc-tag">{c["tag"]} <span aria-hidden="true">&rarr;</span></span></a>'
    assert dead in hub, c["name"]
    hub = hub.replace(dead, live)
hub = hub.replace("We're building a local guide for each of our neighboring communities &mdash; <a href=\"verona-wi.html\">Verona's guide</a> is live now, with the rest on the way.",
                  "Every community has its own local guide &mdash; tap any name above, or start with <a href=\"verona-wi.html\">Verona, our hometown</a>.")
open("service-areas.html", "w").write(hub)
print("hub rows linked")
