"""Provenance LA seed run, Beverly Hills area, 2026-10-09.
All restaurant evidence below was read with Tavily (extract/search) on 2026-10-09.
Coordinates: OpenStreetMap (Overpass) where mapped, otherwise Nominatim geocodes."""

TODAY = "2026-10-09"
FETCHED = "2026-10-09T16:00:00Z"

NEIGHBORHOODS = {
    "90210": "Beverly Hills · Golden Triangle",
    "90212": "Beverly Hills · South Beverly",
    "90211": "Beverly Hills · Restaurant Row",
    "90048": "Beverly Grove / West 3rd",
    "90069": "West Hollywood (west)",
    "90067": "Century City",
    "90035": "Pico-Robertson",
}
SLICES = {
    "Beverly Hills (city)": ["90210", "90212", "90211"],
    "Beverly Grove & West Hollywood": ["90048", "90069"],
    "Century City & Pico-Robertson": ["90067", "90035"],
}
CITY = {"90210": "Beverly Hills", "90212": "Beverly Hills", "90211": "Beverly Hills",
        "90048": "Los Angeles", "90069": "West Hollywood", "90067": "Los Angeles", "90035": "Los Angeles"}

SM_LIST = "https://www.santamonica.gov/farmers-market-vendors"
BH_LIST = "https://www.beverlyhills.org/DocumentCenter/View/9244/Farmers--Vendors"

# producer_id: (name, type, category, city, state, tier, tier_basis, flags, website, notes)
PRODUCERS = {
    "L001": ("Weiser Family Farms", "farm", "produce", "Tehachapi", "CA", "P4",
             "Named, no certification record matched. The farm describes its own practices as sustainable; the Santa Monica Farmers Market lists it without an ORGANIC designation",
             ["sm-market-vendor"], "https://www.weiserfamilyfarms.com",
             "A 2016 profile said the farm was 'in the process of becoming certified organic'; no current certification statement was found on the farm's own site. Named by two restaurants in this run."),
    "L002": ("Tutti Frutti Farms", "farm", "produce", "Lompoc", "CA", "P4",
             "Named, registry not yet matched. The Santa Monica Farmers Market vendor list designates it ORGANIC, which is a lead to confirm in USDA INTEGRITY, not a tier by itself",
             ["sm-market-organic"], "", ""),
    "L003": ("See Canyon Farm", "farm", "produce", "San Luis Obispo County", "CA", "P4",
             "Named, no certification record matched. Listed by the Santa Monica Farmers Market without an ORGANIC designation",
             ["sm-market-vendor"], "", ""),
    "L004": ("Polito Family Farms", "farm", "produce", "Valley Center", "CA", "P4",
             "Named, no certification record matched. Listed by the Santa Monica Farmers Market without an ORGANIC designation",
             ["sm-market-vendor"], "", "Spago's menu says \"Polito Farms\"; matched to the Santa Monica market vendor of that family name."),
    "L005": ("Munak Ranch", "farm", "produce", "", "CA", "P4",
             "Named, no certification record matched. Listed (seasonal) by the Santa Monica Farmers Market without an ORGANIC designation",
             ["sm-market-vendor"], "", ""),
    "L006": ("Kenter Canyon Farms", "farm", "produce", "Fillmore", "CA", "P4",
             "Named, registry not yet matched. The farm's own site says it is certified organic and the Santa Monica Farmers Market designates it ORGANIC; both are leads to confirm in USDA INTEGRITY",
             ["self-declared-organic", "sm-market-organic", "bh-market-vendor"], "https://www.kentercanyonfarms.com",
             "Farmhouse's site names \"Nathan's family farm\" without naming it; press coverage identifies Executive Farmer Nathan Peitso's family farm as Kenter Canyon Farms, so the alias is recorded as unconfirmed. The farm says it grows '100% certified organic herbs, lettuces, seasonal vegetables' plus organic winter wheat in Imperial Valley."),
    "L007": ("Smith Farms", "farm", "produce", "", "CA", "P4",
             "Named, registry not yet matched. A Santa Monica Farmers Market vendor called Smith Farms is designated ORGANIC, but the menu's \"Smith Farm's lettuce\" has not been confirmed as that farm",
             ["sm-market-organic", "registry-ambiguous"], "",
             "Common farm name; match to the Santa Monica market vendor is unconfirmed pending a check with the restaurant."),
    "L008": ("Schaner Farms", "farm", "produce", "Valley Center", "CA", "P4",
             "Named by first name only; alias unconfirmed. Listed by the Santa Monica Farmers Market without an ORGANIC designation",
             ["sm-market-vendor"], "",
             "A.O.C.'s menu says \"peter's cipollini onions\" and \"peter's onion panade\". Peter Schaner of Schaner Farms is the likeliest match; unconfirmed."),
    "L009": ("Flora Bella Farm", "farm", "produce", "Three Rivers", "CA", "P4",
             "Named by first name only; alias unconfirmed. No certification record matched",
             [], "",
             "A.O.C. lists \"james' rapini\". James Birch of Flora Bella Farm is a long-time A.O.C. grower per press; unconfirmed on the restaurant's own pages."),
    "L010": ("Andante Dairy", "farm", "dairy", "Petaluma", "CA", "P4",
             "Named, not yet verified", [], "", ""),
    "L011": ("Snake River Farms", "brand", "meat", "Boise", "ID", "P4",
             "Named, not yet verified. A beef and pork brand of Agri Beef rather than a single farm", [], "", ""),
    "L012": ("Liberty Ducks (Sonoma County Poultry)", "farm", "meat", "Penngrove", "CA", "P4",
             "Named, not yet verified", [], "", "Menu says \"Liberty Duck Breast\"."),
    "L013": ("Laura Chenel", "processor", "dairy", "Sonoma", "CA", "P4",
             "Named, not yet verified. A creamery that buys goat milk from partner farms", [], "https://laurachenel.com", ""),
    "L014": ("First Light Farms", "coop", "meat", "Hawke's Bay", "NZ", "P4",
             "Named, not yet verified for organic. First Light states it holds Certified Humane accreditation (an animal-welfare program, not an organic certification)",
             ["coop", "certified-humane"], "https://www.firstlight.farm/us",
             "A collective of New Zealand farmers raising grass-fed Wagyu. matū says it serves this beef exclusively."),
    "L015": ("Westholme", "brand", "meat", "", "AU", "P4",
             "Named, not yet verified. An Australian Wagyu brand rather than a single farm", [], "", "Mastro's menu: \"Australian Wagyu Westholme Cross Cattle\"."),
    "L016": ("WinterFrost", "brand", "meat", "", "", "P4",
             "Named, not yet verified. Identity of the producer behind the brand not yet established", [], "", "Mastro's menu: \"American Wagyu WinterFrost Halal\"."),
    "L017": ("Rabbi's Daughter", "brand", "meat", "", "", "P4",
             "Named, not yet verified. A kosher beef brand", [], "", ""),
    "L018": ("Certified Angus Beef", "brand program", "meat", "Wooster", "OH", "P5-opaque",
             "Brand program pass-through; the chain stops here. Certified Angus Beef is a breed-and-grade specification licensed to many packers, so it does not identify a ranch",
             [], "", ""),
}

# name, address, zip, cuisine, lat, lng, website, sample, mode, notes, pages, suppliers[(pid, name_raw, alias_confirmed, context, products, source_url)]
AOC_MENU = "https://www.aocwinebar.com/menus"
SPAGO_MENU = "https://www.opentable.com/spago-beverly-hills"
SPAGO_CTX = ("Tutti Frutti Farms Heirloom Tomatoes — See Canyon Farm's Apricots | Pistachio Crusted Chevre | Polito Farms Tiger Figs | Sicilian Olive Oil [...] "
             "Barchette Pasta — Munak Ranch Sungold Tomatoes | Maine Lobster | Charred Shishito Peppers [...] Line Caught Tai Snapper — Maine Lobster | Weiser Farm's Summer Squash | Confit Cherry Tomatoes [...] "
             "Laquered Liberty Duck Breast — Plum Mostarda | Weiser Farms Baby Carrots | Summer Squash [...] Grilled Snake River Farms Wagyu New York Striploin")
SPAGO_PIZZA = "Prosciutto San Daniele Pizza — Roasted Jimmy Nardello Sweet Peppers | Andante Dairy Chevre | Parsley | Garlic Confit | Wilted Spinach | Reduced Grape Must"
AOC_CTX = ("FOCACCIAS [...] chanterelles, red kabocha, peter's cipollini onions & raclette [...] grilled hanger steak, peter's onion panade & au poivre butter 38 [...] "
           "vegetables and… slow-roasted romano beans, quince paste & marconas 18 · crushed weiser potatoes, crème fraîche & chives 16")
MASTROS_URL = "https://www.mastrosrestaurants.com/location/mastros-steakhouse-beverly-hills"
MASTROS_CTX = ("American Wagyu — WinterFrost Halal — Filet 7oz $99 · Boneless Ribeye 16oz $120 — Australian Wagyu — Westholme Cross Cattle — Tomahawk Chop 32oz [...] "
               "Rabbi's Daughter Kosher Bone-In Ribeye 16oz $95")

RESTAURANTS = [
    # ---------- C: names producers ----------
    dict(id="c01", name="Spago", address="176 N Canon Dr", zip="90210", cuisine="Californian", lat=34.0676650, lng=-118.3978072,
         website="https://wolfgangpuck.com/restaurants/spago-beverly-hills", sample="curated", mode="published", claims=True, pages=2,
         sourcing_url=SPAGO_MENU,
         notes="Spago's own page claims 'the freshest local ingredients … the best of California's markets' and lists no farms. The farms below come from the dinner menu Spago publishes to OpenTable (last updated 2026-08-08).",
         suppliers=[("L002", "Tutti Frutti Farms", True, SPAGO_CTX, ["heirloom tomatoes"], SPAGO_MENU),
                    ("L003", "See Canyon Farm's", True, SPAGO_CTX, ["apricots"], SPAGO_MENU),
                    ("L004", "Polito Farms", True, SPAGO_CTX, ["tiger figs"], SPAGO_MENU),
                    ("L005", "Munak Ranch", True, SPAGO_CTX, ["sungold tomatoes"], SPAGO_MENU),
                    ("L001", "Weiser Farm's / Weiser Farms", True, SPAGO_CTX, ["summer squash", "baby carrots"], SPAGO_MENU),
                    ("L010", "Andante Dairy", True, SPAGO_PIZZA, ["chèvre"], SPAGO_MENU),
                    ("L011", "Snake River Farms", True, SPAGO_CTX, ["wagyu beef"], SPAGO_MENU),
                    ("L012", "Liberty Duck", True, SPAGO_CTX, ["duck breast"], SPAGO_MENU)]),
    dict(id="c02", name="A.O.C. West Hollywood", address="8700 W 3rd St", zip="90048", cuisine="Mediterranean / wine bar", lat=34.07346, lng=-118.38186,
         website="https://www.aocwinebar.com", sample="curated", mode="published", claims=True, pages=2, sourcing_url=AOC_MENU,
         notes="Menus name growers by first name (\"peter's\", \"james'\") or surname (\"weiser\"). Only Weiser is unambiguous; the other two are recorded as unconfirmed aliases. The wine list is described as focused on organic and biodynamic producers (not graded: produce only).",
         suppliers=[("L001", "weiser", True, AOC_CTX, ["potatoes"], AOC_MENU),
                    ("L008", "peter's", False, AOC_CTX, ["cipollini onions"], AOC_MENU),
                    ("L009", "james'", False, "happy hour bites [...] green quinoa dumplings 18 · spanish fried chicken 19 · james' rapini, taleggio, cantimpalo & piri piri focaccia 18", ["rapini"], "https://www.aocwinebar.com/about-aoc")]),
    dict(id="c03", name="Farmhouse", address="8500 Beverly Blvd, Ste 113", zip="90048", cuisine="Californian", lat=34.07572, lng=-118.37705,
         website="https://farmhousela.com", sample="curated", mode="published", claims=True, pages=1, sourcing_url="https://farmhousela.com",
         notes="Owned and run by Executive Farmer Nathan Peitso. The site refers to 'his family farm' and 'the region's top farmers' without naming them; the family farm is Kenter Canyon Farms per press, so the name match is unconfirmed.",
         suppliers=[("L006", "Nathan's family farm", False,
                     "At FARMHOUSE, our Executive Farmer, Nathan Peitso, works directly with his family farm and the region's top farmers to grow, harvest, and create seasonal and vibrant dishes. The grain used for the pasta, pizza and bread comes from Nathan's family farm.",
                     ["grain", "greens"], "https://farmhousela.com")]),
    dict(id="c04", name="Prospect Gourmand", address="107 N Robertson Blvd", zip="90211", cuisine="Californian", lat=34.0672091, lng=-118.3837876,
         website="https://www.prospectgourmand.com", sample="curated", mode="published", claims=True, pages=2, sourcing_url="https://www.prospectgourmand.com/menu",
         notes="Homepage claims 'strong relationships with nearby farms and producers' without naming any; the brunch menu names two.",
         suppliers=[("L007", "Smith Farm's", False, "Farmers Market Salad — Persimmons, organic wild arugula, Smith Farm's lettuce, blue cheese, red onion.", ["lettuce"], "https://www.prospectgourmand.com/menu"),
                    ("L013", "Laura Chenel", True, "Teasers — Laura Chenel Goat Cheese — Marinated in olive oil and herbs, seasonal fruit, grilled bread.", ["goat cheese"], "https://www.prospectgourmand.com/menu")]),
    dict(id="c05", name="matū", address="239 S Beverly Dr, Ste 100", zip="90212", cuisine="Steakhouse", lat=34.0638817, lng=-118.3991719,
         website="https://www.matusteak.com", sample="curated", mode="published", claims=False, pages=2, sourcing_url="https://www.matusteak.com/about-us/our-journey",
         notes="Single-source beef, named on every page. No produce supplier named.",
         suppliers=[("L014", "First Light Farms", True, "Steak restaurants exclusively serving 100% grass-fed Wagyu from First Light Farms.", ["wagyu beef"], "https://www.matusteak.com")]),
    dict(id="n5282642760", name="Mastro's Steakhouse", address="246 N Canon Dr", zip="90210", cuisine="Steakhouse", lat=34.0688, lng=-118.39879,
         website=MASTROS_URL, sample="osm", mode="published", claims=False, pages=1, sourcing_url=MASTROS_URL,
         notes="Beef brands named on the menu; Japanese wagyu is identified by prefecture only. 'Organic Lemon Pepper Chicken' names no farm.",
         suppliers=[("L016", "WinterFrost", True, MASTROS_CTX, ["wagyu beef"], MASTROS_URL),
                    ("L015", "Westholme", True, MASTROS_CTX, ["wagyu beef"], MASTROS_URL),
                    ("L017", "Rabbi's Daughter", True, MASTROS_CTX, ["kosher ribeye"], MASTROS_URL)]),
    dict(id="n12662791401", name="Lawry's The Prime Rib", address="100 N La Cienega Blvd", zip="90211", cuisine="Steakhouse", lat=34.0678, lng=-118.37607,
         website="https://www.lawrysonline.com/lawrys-the-prime-rib-beverly-hills/", sample="osm", mode="published", claims=False, pages=1,
         sourcing_url="https://www.lawrysonline.com/lawrys-the-prime-rib-beverly-hills/",
         notes="Names a beef brand program, not a ranch.",
         suppliers=[("L018", "Certified Angus Beef® brand", True, "The unique menu features our Roasted Prime Ribs of Beef served table-side from gleaming silver carts. Proudly serving Certified Angus Beef® brand for over 30 years.", ["beef"], "https://www.lawrysonline.com/lawrys-the-prime-rib-beverly-hills/")]),
]

# ---------- D: claims, no names ----------
D = [
    ("n5473240828", "Gracias Madre", "8905 Melrose Ave", "90069", "Vegan Mexican", 34.08096, -118.38695, "https://graciasmadre.com/", "osm",
     "\"traditional Mexican cuisine made from scratch using organic, non-GMO, plant-based ingredients sourced from local and regenerative farmers\". No farm named on the home or menu pages."),
    ("n5207270076", "Kreation Organic Juicery (West Hollywood)", "8910 Santa Monica Blvd", "90069", "Juice / café", 34.08442, -118.38433, "https://www.kreationjuice.com/", "osm",
     "\"raw, local, high-quality products\"; organic named on products. No farm named."),
    ("n11298663969", "Kreation Organic (Beverly Hills)", "9465 Charleville Blvd", "90212", "Juice / café", 34.0651, -118.39951, "https://www.kreationjuice.com/", "osm",
     "Same site as the West Hollywood shop: \"raw, local, high-quality products\". No farm named."),
    ("n10181663271", "Tocaya Organica", "10250 Santa Monica Blvd", "90067", "Mexican", 34.05793, -118.41869, "https://www.tocaya.com/", "osm",
     "\"Thoughtfully Sourced & Made Right … Our leafy produce is sourced responsibly\"; meat and fish free of hormones and antibiotics. No producer named."),
    ("n11051511152", "The Butcher's Daughter", "8755 Melrose Ave", "90069", "Plant-forward café", 34.08099, -118.38488, "https://www.thebutchersdaughter.com", "osm",
     "\"nourishing, seasonal dishes … organic cold-pressed juices\". No farm named."),
    ("n1898409081", "Urth Caffé (Beverly Hills)", "267 S Beverly Dr", "90212", "Café", 34.06265, -118.39934, "https://www.urthcaffe.com/", "osm",
     "\"Exclusively Heirloom Organic Coffee & Fine Tea\". No farm or estate named on the pages read."),
    ("n1028939687", "Urth Caffé (Melrose)", "8565 Melrose Ave", "90069", "Café", 34.08207, -118.37885, "https://www.urthcaffe.com/", "osm",
     "Same site as Beverly Hills: \"Exclusively Heirloom Organic Coffee & Fine Tea\". No farm named."),
    ("n7439796285", "Comoncy", "413 N Bedford Dr", "90210", "Café", 34.06792, -118.40532, "https://www.comoncy.com/", "osm",
     "\"a focus on locally sourced, sustainable, and organic ingredients\". No farm named."),
    ("n7487489786", "ecco un poco", "8318 W 3rd St", "90048", "Gelato", 34.07257, -118.37076, "https://www.eccounpoco.com/", "osm",
     "\"made with premium Italian and local ingredients\". No producer named."),
    ("n7241158811", "Natalee Thai", "998 S Robertson Blvd", "90035", "Thai", 34.05975, -118.38341, "https://nataleethai.com", "osm",
     "\"using fresh local products whenever possible\". No producer named."),
    ("n11294384169", "Parakeet Cafe", "206 S Beverly Dr", "90212", "Café", 34.06474, -118.39891, "https://www.parakeetcafe.com/", "osm",
     "\"every item on our menu is full of lush, organic ingredients\". No farm named."),
    ("w365025332", "Flavor of India", "9045 Santa Monica Blvd", "90069", "Indian", 34.08215, -118.38848, "https://www.flavorofindia.com/", "osm",
     "\"We source locally … locally sourced meats and spices\". No producer named."),
    ("n4985436567", "Il Pastaio", "400 N Canon Dr", "90210", "Italian", 34.07085, -118.40082, "https://www.ilpastaiobeverlyhills.com", "osm",
     "Private-dining guidelines: \"farm fresh menus … ample opportunity to source all our farm fresh ingredients\". No farm named; homepage did not load."),
    ("c06", "Sweetgreen (Beverly + Wilshire)", "251 N Beverly Dr", "90210", "Salads", 34.0677463, -118.3998715, "https://www.sweetgreen.com/locations/beverly-wilshire", "curated",
     "\"We partner with local farms\"; organic kale and spinach on the menu. No partner farm named on the location or menu pages."),
]

# ---------- E: nothing disclosed ----------
E = [
    ("c07", "CUT", "9500 Wilshire Blvd", "90212", "Steakhouse", 34.0668881, -118.4003735, "https://wolfgangpuck.com/restaurants/cut-beverly-hills", "curated",
     "\"the finest beef from regions across the globe\"; no producer and no local or organic claim on the page read."),
    ("n12492431745", "Funke", "9388 S Santa Monica Blvd", "90210", "Italian", 34.07181, -118.40151, "https://www.funkela.com/", "curated",
     "Nothing on the restaurant's own site. Press video shows the chef buying at the Santa Monica Farmers Market, but third-party coverage is not counted."),
    ("w425375824", "Matsuhisa", "129 N La Cienega Blvd", "90211", "Japanese", 34.06835, -118.3766, "https://matsuhisabeverlyhills.com/", "osm", ""),
    ("n3921154400", "Joan's on Third", "8350 W 3rd St", "90048", "Café & market", 34.07281, -118.37178, "https://www.joansonthird.com", "curated", ""),
    ("n11409024402", "Manzke", "9575 W Pico Blvd", "90035", "Fine dining", 34.0554, -118.39764, "https://manzkehospitalitygroup.com/manzke", "curated",
     "\"hyper-seasonal ingredients sourced from the finest purveyors available\". Not a local or organic claim, and no purveyor named."),
    ("c08", "Craig's", "8826 Melrose Ave", "90069", "American", 34.0806987, -118.3858130, "https://www.craigs.la", "curated", ""),
    ("n6835510455", "Hinoki & the Bird", "10 W Century Dr", "90067", "Californian-Asian", 34.05654, -118.41517, "https://www.hinokiandthebird.com/", "osm", ""),
    ("n5077444022", "Zinqué", "8684 Melrose Ave", "90069", "French café", 34.08129, -118.38265, "https://www.lezinque.com/", "osm", ""),
    ("n5207270078", "Yoshiharu Ramen", "8908 Santa Monica Blvd", "90069", "Ramen", 34.08446, -118.38426, "https://www.yoshiharuramen.com/", "osm", ""),
    ("n5217220921", "Via Alloro", "301 N Canon Dr", "90210", "Italian", 34.06924, -118.39982, "https://www.viaalloro.com/", "osm", ""),
    ("n5246349719", "Chop Stop", "8717 Santa Monica Blvd", "90069", "Salads", 34.08743, -118.38075, "https://chopstop.com/", "osm", ""),
    ("n5211100936", "zpizza", "8943 Santa Monica Blvd", "90069", "Pizza", 34.08422, -118.38549, "https://zpizzaweho.com/", "osm",
     "Only beverage sourcing is described (\"Wander + Ivy, organic wines made with certified organic grapes\"); nothing on food."),
    ("n5247316897", "Fresh Brothers", "8613 Santa Monica Blvd", "90069", "Pizza", 34.08797, -118.37963, "https://www.freshbrothers.com/", "osm", ""),
    ("n5852254960", "Croft Alley", "9433 Brighton Way", "90210", "Café", 34.07027, -118.40167, "https://croftalley.com/", "osm", ""),
    ("n6175531585", "Fogo de Chão", "133 N La Cienega Blvd", "90211", "Brazilian steakhouse", 34.06867, -118.3766, "https://fogodechao.com/location/beverly-hills/", "osm", ""),
    ("n7234311185", "Lazy Daisy", "155 S Robertson Blvd", "90211", "American", 34.06578, -118.38381, "https://www.eatlazydaisy.com", "osm", ""),
    ("n7248550479", "La Provence Patisserie & Cafe", "8950 W Olympic Blvd", "90211", "French café", 34.05905, -118.38742, "https://laprovencecafe.com/", "osm", ""),
    ("n7399932386", "Bombay Palace", "8690 Wilshire Blvd", "90211", "Indian", 34.06625, -118.38121, "https://www.bombaypalace.com/", "osm", ""),
    ("n7578932785", "Ferrarini", "9622 Brighton Way", "90210", "Italian café", 34.06819, -118.40425, "https://www.ferrarinicafebh.com/", "osm", ""),
    ("n9371481379", "Very Thai", "10250 Santa Monica Blvd", "90067", "Thai", 34.05894, -118.41999, "https://verythaiusa.com/", "osm", ""),
    ("n9371481380", "Ramen Nagi", "10250 Santa Monica Blvd", "90067", "Ramen", 34.05917, -118.41963, "https://ramennagiusa.com/", "osm", ""),
    ("n10181663272", "HRB", "10250 Santa Monica Blvd", "90067", "Sushi", 34.058, -118.4189, "https://www.thehrbexperience.com/", "osm", ""),
    ("n9230973890", "Seabutter", "9105 W Olympic Blvd", "90212", "Sushi", 34.05955, -118.39007, "https://seabuttersushi.com/", "osm", ""),
    ("n9461964204", "Beverliz Cafe", "308 S Beverly Dr", "90212", "Mediterranean café", 34.06179, -118.39892, "http://www.beverlizcafe.com/", "osm", ""),
    ("n10709960518", "Mr Chow", "344 N Camden Dr", "90210", "Chinese", 34.06807, -118.40332, "https://www.mrchow.com/location/beverly-hills/", "osm", ""),
    ("n11294384770", "Piccolo Paradiso", "150 S Beverly Dr", "90212", "Italian", 34.06546, -118.39891, "https://piccoloparadisobeverlyhills.com/", "osm", ""),
    ("n13566413576", "Il Cielo", "9018 Burton Way", "90211", "Italian", 34.07186, -118.38837, "https://www.ilcielo.com/", "osm", ""),
    ("n13337212904", "Meizhou Dongpo", "10250 Santa Monica Blvd", "90067", "Chinese", 34.05796, -118.41925, "https://www.mzdpusa.com/", "osm", ""),
    ("n11535809537", "Alfred Coffee", "490 N Beverly Dr", "90210", "Coffee", 34.07162, -118.40338, "https://www.alfred.la/", "osm", ""),
    ("n12710897648", "Miura", "9480 Dayton Way", "90210", "Sushi omakase", 34.06742, -118.40059, "https://sushiyamamoto-beverlyhills.com", "osm",
     "Mapped in OSM as Sushi Yamamoto; the site now presents Miura. \"wild seafood … primarily from Japan\"; no producer named."),
    ("w557689265", "Katsuya", "10250 Santa Monica Blvd", "90067", "Japanese", 34.05954, -118.42005, "https://www.sbe.com/restaurants/katsuya/katsuya-century-city/", "osm", ""),
    ("n14018897901", "Nagila Pizza", "9411 W Pico Blvd", "90035", "Kosher pizza", 34.05554, -118.39423, "https://nagilarestaurant.com/", "osm", ""),
    ("n1028934811", "Roni's", "9911 S Santa Monica Blvd", "90212", "Diner", 34.06534, -118.41228, "https://www.ieatatronis.com/", "osm",
     "Only the beer list is described as 'locally sourced'; nothing on food."),
]

# Attempted but not graded
NOT_CRAWLED = [
    ("Bossa Nova", "site did not load"), ("La Dolce Vita", "site did not load"), ("Roxbury Cafe", "site did not load"),
    ("Panini Cafe", "site timed out"), ("The Palm Beverly Hills", "location page 404"), ("Boa Steakhouse", "location page 404"),
    ("Guisados", "site did not load"), ("Nori", "location page 404"), ("Demitasse", "location page 404"), ("Prova", "site did not load"),
    ("Greenwich Village Pizza", "site did not load"), ("Phonomenal", "site did not load"), ("Shanghai Grill", "site did not load"),
    ("The Assembly", "site 404"), ("Catch LA", "location page 404"), ("The Bazaar by José Andrés", "location page 404"),
    ("Summer Fish & Rice", "site did not load"), ("Ruth's Chris Steak House", "site did not load"), ("Brighton Coffee Shop", "site did not load"),
    ("CAVA Century City", "site did not load"), ("208 Rodeo", "site did not load"), ("Commissary", "site did not load"),
    ("Dan Tana's", "site did not load"), ("La Conversation", "site did not load"), ("Nate 'n Al's", "site did not load"),
    ("The Polo Lounge", "site did not load"), ("Fig & Olive", "site did not load"), ("Cecconi's West Hollywood", "URL now serves a different Cecconi's"),
    ("The Cheesecake Factory", "only a store locator returned"), ("Cousins Maine Lobster", "only a store locator returned"),
    ("Craft Los Angeles", "site did not load; not listed in the chef's current restaurant group"),
    ("Joss Cuisine", "domain lapsed (now unrelated content)"), ("Fresh Corn Grill", "domain lapsed (now unrelated content)"),
    ("Rawberri", "domain lapsed (now unrelated content)"), ("Sushi by H", "domain lapsed (now unrelated content)"),
    ("Cafe Istanbul", "domain lapsed (now unrelated content)"), ("Citizen", "domain lapsed (now unrelated content)"),
    ("Hedley's", "domain lapsed (now unrelated content)"), ("Bicyclette", "domain lapsed (now unrelated content)"),
    ("Cal Mare", "domain lapsed (now unrelated content)"),
]
CLOSED = [
    ("The Farm of Beverly Hills", "site says last day of service was 2025-03-03"), ("Walter's Cafe", "site announces closure"),
    ("The Stinking Rose (LA)", "site now lists San Francisco only"), ("Tatel Beverly Hills", "group site no longer lists Beverly Hills"),
    ("Cantina Frida", "temporarily closed for a remodel"), ("Toca Madera West Hollywood", "group site lists AZ, NV, TX only"),
    ("Zinc Café (West Hollywood)", "group site no longer lists West Hollywood"),
]
