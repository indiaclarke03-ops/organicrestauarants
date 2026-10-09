# Provenance: restaurant sourcing transparency

Static, single-file sites that grade restaurants on **how much of their sourcing they disclose and how much of it is verified**, never on how virtuous it sounds. Each named producer gets a tier (P1 USDA certified organic … P4 named, not yet verified … P5 distributor), and each restaurant a grade A–E from published thresholds.

| Area | Page | Seed run |
|---|---|---|
| New York City (Lower Manhattan, Tribeca/Flatiron/Chelsea, North Brooklyn, Fort Greene and around) | [`nyc/index.html`](nyc/index.html) | 2026-09-16, 144 restaurants |
| Los Angeles: Beverly Hills area (Beverly Hills, Beverly Grove, western West Hollywood, Century City, Pico-Robertson) | [`la/index.html`](la/index.html) | 2026-10-09, 57 restaurants (2 passes) |

Open either `index.html` in a browser; everything (data, street basemap, app) is inline.

## LA run notes

- **Universe:** 193 restaurants and cafés mapped in OpenStreetMap in the study area (Overpass API). Every one with a website was attempted (the "OpenStreetMap census"), plus curated farm-forward and fine-dining picks.
- **Reading:** restaurant sites and menus were read with [Tavily](https://tavily.com) search/extract/crawl. Verbatim producer-naming sentences are kept as evidence. Spago's farms come from the menu it publishes to OpenTable, since its own page lists none.
- **Pass 2 (menus):** went back for actual menus (PDFs, menu pages, OpenTable-syndicated menus, the restaurant's own social posts). New disclosures at Gracias Madre (Kernel of Truth masa), Sweetgreen (Clark Street Bakery), Baldi, Gemma, CUT and Ardor.
- **Verification ladder (LA):** P1 = certifier/registry record (Tutti Frutti Farms via the CCOF member directory). P3 = *judged organic* on reasonable evidence: the farm, or a buyer, distributor or market that deals with it, says it is organic or farms without synthetic pesticides/fertilisers, and nothing contradicts it. Every source is quoted on the producer page; uncertified farms are flagged. P1–P3 all count as verified for grades. USDA INTEGRITY itself still could not be queried.
- **Result:** 2 B (Spago 4 of 5 produce growers verified or judged organic; Farmhouse via Kenter Canyon Farms) · 11 C · 12 D · 32 E. 29 named producers: 1 P1, 6 P3, 21 P4, 1 P5. Zuckerman's Farm (Ardor) is documented conventional.
- `la/data.json` is the generated dataset; `la/pipeline/` holds the hand-curated evidence (`la_data.py`, `la_pass2.py`) and the build script, which uses the NYC page as its template.
