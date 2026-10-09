"""Pass 2 (2026-10-09): menu re-scrape + supplier verification, with the loosened verification rule.

Verification ladder used from pass 2 on:
  P1  registry record: certifier directory or USDA INTEGRITY shows Certified, crops scope.
  P2  peer certification listing (CNG, Real Organic Project, ROC, Demeter).
  P3  judged organic: reasonable-judgement standard. Needs (a) a statement that the farm is organic, or farms without
      synthetic pesticides and fertilisers, from the farm itself or a buyer/distributor/market that deals with it, and
      (b) no contradicting record (e.g. a distributor listing it as conventional). Each source is shown on the producer page.
  P4  named, not enough evidence either way (or contradicted).
P1, P2 and P3 count as verified for restaurant grades. Aliases are confirmed by reasonable judgement where independent
sources tie a first name or description to one farm.
"""

CHECKED = "2026-10-09"

# pid -> overrides applied to the pass-1 producer record
OVERRIDES = {
    "L002": dict(tier="P1", tier_basis="Registry record: CCOF Certification Services lists Tutti Frutti Farms as Certified under the USDA NOP, Crops scope certified since 27 Oct 1997 (client sc079, 321 acres)",
                 certifier="CCOF Certification Services, LLC", op_status="Certified", status_effective="10/27/1997",
                 scopes_certified="USDA NOP:Certified;CROPS:Certified;HANDLING:Certified (12/01/2010)",
                 alt_cert_url="https://ccof.org/directory-member/tutti-frutti-farms", integrity_checked=CHECKED,
                 judgement=[("CCOF member directory", "https://ccof.org/directory-member/tutti-frutti-farms", "USDA NOP: Certified, 27 Oct 1997 · Crops: Certified, 27 Oct 1997 · Handling: Certified, 1 Dec 2010 · client code sc079"),
                            ("Farm website", "https://tuttifrutti.com", "\"All Tutti Frutti Farms produce is certified by CCOF\"; family-owned and certified organic since 1988")]),
    "L006": dict(tier="P3", tier_basis="Judged organic. The farm states it is certified organic, the Santa Monica Farmers Market designates it ORGANIC, and its sister mill describes certified organic farming; no contrary record. No certifier record matched yet, so not P1",
                 judgement=[("Farm website", "https://www.kentercanyonfarms.com/history", "\"we grow 100% certified organic herbs, lettuces, seasonal vegetables, six varieties of avocados, lemons, and oranges\""),
                            ("City of Santa Monica Farmers Market vendor list", "https://www.santamonica.gov/farmers-market-vendors", "\"Kenter Canyon Farms - ORGANIC (WED, SAT)\""),
                            ("Roan Mills (sister bakery)", "https://roanmills.com/farmer1", "\"Roan Mills was born in 2013 as a new branch of our family farm, Kenter Canyon Farms … regenerative and certified organic farming practices\""),
                            ("CCOF directory", "https://ccof.org/directory-member/kenter-canyon-farms", "No CCOF listing under this name; certifier not identified")]),
    "L003": dict(tier="P3", tier_basis="Judged organic in practice, not certified. Its distributor describes a dry farm using no chemical fertilizers or pesticides; no contrary record",
                 flags_add=["uncertified-organic-practices"],
                 judgement=[("FreshPoint (distributor) farm profile", "https://local.freshpoint.com/store_page/see-canyon", "\"On his dry farm, Mike uses no chemical fertilizers nor pesticides\""),
                            ("City of Santa Monica Farmers Market vendor list", "https://www.santamonica.gov/farmers-market-vendors", "Listed without an ORGANIC designation (the market only marks certified vendors)")]),
    "L004": dict(tier="P3", tier_basis="Judged organic in practice, not certified. A produce distributor and an organic caterer both describe the fruit as pesticide-free/organic; no contrary record",
                 flags_add=["uncertified-organic-practices"],
                 judgement=[("Nature's Produce (distributor) market report", "https://www.naturesproduce.com/wp-content/uploads/2018/09/Natures-Produce-Farmers-Market-Update-8-9.pdf", "\"Their fruit is pesticide free and grown here on our farm\""),
                            ("EcoCaters (buyer) farm profile", "https://www.ecocaters.com/blog/polito-family-farms", "\"ORGANIC: Yes\""),
                            ("City of Santa Monica Farmers Market vendor list", "https://www.santamonica.gov/farmers-market-vendors", "Listed without an ORGANIC designation")]),
    "L005": dict(tier="P3", tier_basis="Judged organic in practice, not certified. Its distributor reports the ranch has been chemical-free since 1985 and states plainly that it is not certified; no contrary record",
                 flags_add=["uncertified-organic-practices"],
                 judgement=[("GrubMarket (distributor) farm profile", "https://blog.grubmarket.com/munak-ranch", "\"Munak Ranch has been chemical-free since their inception in 1985 … While they're not certified organic, they practice sustainable growing methods\"; foreman: \"I grow organically\"")]),
    "L001": dict(tier_basis="Named; not judged organic. The farm calls its practices sustainable/regenerative, but no source says it farms without synthetic inputs, and a 2016 plan to certify has no follow-up record. The Santa Monica market lists it without an ORGANIC designation",
                 judgement=[("Farm website", "https://www.weiserfamilyfarms.com/our-story", "\"a bio-diverse farm dedicated to applying sustainable farming techniques\""),
                            ("LA Chef Net, 2016", "https://lachefnet.wordpress.com/2016/07/03/la-chefs-supplier-alexander-weiser-of-weiser-family-farms", "\"in the process of becoming certified organic\" (no later record found)")]),
    "L007": dict(tier="P3", tier_basis="Judged organic: the Santa Monica Farmers Market designates its Smith Farms vendor ORGANIC. The restaurant's \"Smith Farm's lettuce\" is not yet confirmed to be that farm, so it does not count toward the grade",
                 judgement=[("City of Santa Monica Farmers Market vendor list", "https://www.santamonica.gov/farmers-market-vendors", "\"Smith Farms - ORGANIC (MST, WED)\""),
                            ("CCOF directory", "https://www.ccof.org/resources/member-directory", "No Southern California Smith Farms listed")]),
}

NEW_PRODUCERS = {
    "L019": ("Kernel of Truth Organics", "processor", "grains", "Los Angeles", "CA", "P3",
             "Judged organic. A tortilleria whose organic, non-GMO corn is reported by the LA Times and NYT as well as the restaurant; no certifier record matched",
             [], "https://www.kotorganics.com", "Masa and tortillas, not produce, so it does not count toward the produce grade.",
             [("Los Angeles Times, 2019", "https://www.latimes.com/food/la-fo-kernel-of-truth-tortilla-company-east-la-20190704-story.html", "\"the only one to use organic, non-GMO corn\""),
              ("New York Times, 2019", "https://www.nytimes.com/2019/10/07/dining/corn-tortilla-kernel-of-truth-organics.html", "Kernel of Truth Organics profiled as an organic, traditionally nixtamalized tortilla maker")]),
    "L020": ("Clark Street Bakery", "bakery", "bakery", "Los Angeles", "CA", "P4", "Named, not yet verified", [], "", "Named as Sweetgreen's Los Angeles focaccia partner.", []),
    "L021": ("Zuckerman's Farm", "farm", "produce", "Stockton", "CA", "P4",
             "Named; documented as conventional. Its distributor FreshPoint lists the farm's asparagus as Conventional",
             ["documented-conventional"], "", "",
             [("FreshPoint (distributor) farm profile", "https://local.freshpoint.com/store_page/zuckermans-farm", "\"Stockton, CA … Conventional … Asparagus\"")]),
    "L022": ("Blackhawk Farms", "farm", "meat", "", "KY", "P4", "Named, not yet verified", [], "", "", []),
    "L023": ("Abatti Ranch", "farm", "meat", "", "CA", "P4", "Named, not yet verified", [], "", "Menu says \"Abatti Ranch, San Diego, California\".", []),
    "L024": ("Sher Wagyu", "brand", "meat", "", "AU", "P4", "Named, not yet verified. An Australian Wagyu brand", [], "", "", []),
    "L025": ("Mizusako Farm", "farm", "meat", "Kagoshima", "JP", "P4", "Named, not yet verified", [], "", "", []),
    "L026": ("Double R Ranch", "brand", "meat", "", "WA", "P4", "Named, not yet verified. A beef brand of Agri Beef", [], "", "", []),
    "L027": ("Mary's Free Range Chicken", "farm", "meat", "Sanger", "CA", "P4", "Named, not yet verified. The brand has certified organic lines, but the menu does not say which product is used", [], "", "", []),
    "L028": ("Fiscalini Farmstead", "farm", "dairy", "Modesto", "CA", "P4", "Named, not yet verified", [], "", "", []),
    "L029": ("Stone Axe", "brand", "meat", "", "AU", "P4", "Named, not yet verified. An Australian Wagyu brand", [], "", "", []),
}

# restaurants whose aliases are now confirmed by reasonable judgement
ALIAS_CONFIRM = {("c03", "L006"): "Farmhouse's site names Executive Farmer Nathan Peitso's \"family farm\"; Roan Mills and multiple press reports identify that farm as Kenter Canyon Farms."}

BALDI_URL = "https://waldorfastoriabeverlyhills.com/wp-content/uploads/2026/08/Baldi-Dinner-Menu-8.13.pdf"
BALDI_CTX = ("Tenderloin 125 — 8oz, Blackhawk Farms, Kentucky · Ribeye 165 — 12oz, Abatti Ranch, San Diego, California · AUSTRALIAN WAGYU — New York 185 — 14oz, Sher Wagyu [...] "
             "JAPANESE WAGYU — Mizusako Farm, Kagoshima Prefecture — New York Strip 55/oz")
GEMMA_URL = "https://waldorfastoriabeverlyhills.com/wp-content/uploads/2026/07/Gemma-All-Day-Menu-7.1.26-1.pdf"
CUT_URL = "https://wolfgangpuck.com/wp-content/uploads/2025/02/CUT-BH_PDRmenu-2.20.2025.pdf"
GM_URL = "https://cdn.shopify.com/s/files/1/0905/4132/6630/files/GM_Menus_-_Web_260930.pdf?v=1791161657"
SG_URL = "https://assets.ctfassets.net/eum7w7yri3zr/76xImBzzZCnvVQ3pDtm9fg/08e451f6d46bb93af2f9694be7f77051/sg-Rosemary_Focaccia_partner.pdf"

# new or upgraded C restaurants (same shape as la_data.RESTAURANTS)
NEW_C = [
    dict(id="c09", name="Baldi", address="9850 Wilshire Blvd (Waldorf Astoria)", zip="90210", cuisine="Tuscan steakhouse", lat=34.0665774, lng=-118.4116409,
         website="https://waldorfastoriabeverlyhills.com/dining/baldi", sample="curated", mode="published", claims=True, pages=2, sourcing_url=BALDI_URL,
         notes="Site: \"hand-selected cuts sourced from individual farms\". The dinner menu (8/13) names the farm or brand for every steak. No produce supplier named.",
         suppliers=[("L022", "Blackhawk Farms", True, BALDI_CTX, ["tenderloin"], BALDI_URL), ("L023", "Abatti Ranch", True, BALDI_CTX, ["ribeye"], BALDI_URL),
                    ("L024", "Sher Wagyu", True, BALDI_CTX, ["wagyu"], BALDI_URL), ("L025", "Mizusako Farm", True, BALDI_CTX, ["wagyu"], BALDI_URL)]),
    dict(id="c10", name="Gemma", address="9850 Wilshire Blvd (Waldorf Astoria)", zip="90210", cuisine="Pan-Asian", lat=34.0667, lng=-118.4114,
         website="https://waldorfastoriabeverlyhills.com/dining/gemma", sample="curated", mode="published", claims=False, pages=2, sourcing_url=GEMMA_URL,
         notes="The all-day menu names a beef brand and a chicken brand. No produce supplier named.",
         suppliers=[("L026", "Double R Ranch", True, "G R I L L — NEW YORK STRIP — 12 OZ, DOUBLE R RANCH 84", ["beef"], GEMMA_URL),
                    ("L027", "Mary's", True, "D I M S U M — MARY'S CHICKEN POTSTICKER, CHILI CRISP PONZU 32", ["chicken"], GEMMA_URL)]),
    dict(id="c07", name="CUT", address="9500 Wilshire Blvd", zip="90212", cuisine="Steakhouse", lat=34.0668881, lng=-118.4003735,
         website="https://wolfgangpuck.com/restaurants/cut-beverly-hills", sample="curated", mode="published", claims=True, pages=2, sourcing_url=CUT_URL,
         notes="The main page names no producer; the private-dining menu (Feb 2025) names a cheese and a wagyu brand and offers a \"Crudité Platter of Santa Monica Vegetables\" (a place, not a farm).",
         suppliers=[("L028", "Fiscalini", True, "Cavatappi Pasta \"Mac & Cheese\" Fiscalini white cheddar | bread crumbs (V)", ["white cheddar"], CUT_URL),
                    ("L029", "Stone Axe", True, "Stone Axe Wagyu Filet Mignon (add $40 per person)", ["wagyu"], CUT_URL)]),
    dict(id="n5473240828", name="Gracias Madre", address="8905 Melrose Ave", zip="90069", cuisine="Vegan Mexican", lat=34.08096, lng=-118.38695,
         website="https://graciasmadre.com/", sample="osm", mode="published", claims=True, pages=3, sourcing_url=GM_URL,
         notes="Claims \"organic, non-GMO ingredients sourced from local farmers\" but names only its tortilla supplier. No produce farm named.",
         suppliers=[("L019", "Kernel of Truth", True, "OUR CORN TORTILLAS ARE MADE IN HOUSE WITH NON-GMO ORGANIC MASA SOURCED FROM KERNEL OF TRUTH", ["masa"], GM_URL)]),
    dict(id="c06", name="Sweetgreen (Beverly + Wilshire)", address="251 N Beverly Dr", zip="90210", cuisine="Salads", lat=34.0677463, lng=-118.3998715,
         website="https://www.sweetgreen.com/locations/beverly-wilshire", sample="curated", mode="published", claims=True, pages=3, sourcing_url=SG_URL,
         notes="\"We partner with local farms\" with no farm named; the only named partner is the regional bakery. The partner PDF pairs bakeries with cities by position, so Clark Street Bakery is matched to Los Angeles by list order.",
         suppliers=[("L020", "Clark Street Bakery", True, "Locally Sourced Near You — We're proud to partner with local bakeries across our regional markets to bring fresh rosemary focaccia to our restaurants. [...] Clark Street Bakery [...] Los Angles, CA", ["focaccia"], SG_URL)]),
    dict(id="c11", name="Ardor", address="9040 Sunset Blvd (West Hollywood EDITION)", zip="90069", cuisine="Vegetable-forward", lat=34.0905472, lng=-118.3888938,
         website="https://www.marriott.com/en-us/dining/restaurant-bar/laxeb-the-west-hollywood-edition/6651753-ardor.mi", sample="curated", mode="published", claims=True, pages=2,
         sourcing_url="https://www.facebook.com/ardorweho/videos/unwrapping-the-taste-of-late-spring-at-ardor-where-fresh-california-sourced-ingr/494904662382927",
         season_note="the only named farm comes from the restaurant's own post of 13 May 2022 and may be out of date",
         notes="Official listing: \"in-house chefs showcase their seasonal market finds from the nearby farmers' markets\". The hotel's own Ardor page now returns 404.",
         suppliers=[("L021", "Zuckerman's Farm", True, "Unwrapping the taste of late spring at Ardor where fresh California sourced ingredients - like asparagus from Zuckerman's Farm - take center stage in Chef John Fraser's seasonally driven menu.", ["asparagus"],
                     "https://www.facebook.com/ardorweho/videos/unwrapping-the-taste-of-late-spring-at-ardor-where-fresh-california-sourced-ingr/494904662382927")]),
]
REMOVE_FROM_DE = {"c07", "n5473240828", "c06"}

NEW_CLOSED = [("Gucci Osteria Beverly Hills", "group site lists Florence, Tokyo and Seoul only"), ("Jean-Georges Beverly Hills", "hotel page removed; the Waldorf now lists Baldi and Gemma")]
NEW_NOT_CRAWLED = [("Bedford & Burns", "domain now unrelated; OpenTable menu blocked"), ("Polo Lounge", "hotel menu page 404; no farm named in indexed pages")]
