# Provenance: restaurant sourcing transparency

Static, single-file sites that grade restaurants on **how much of their sourcing they disclose and how much of it is verified**, never on how virtuous it sounds. Each named producer gets a tier (P1 USDA certified organic … P4 named, not yet verified … P5 distributor), and each restaurant a grade A–E from published thresholds.

| Area | Page | Seed run |
|---|---|---|
| New York City (Lower Manhattan, Tribeca/Flatiron/Chelsea, North Brooklyn, Fort Greene and around) | [`nyc/index.html`](nyc/index.html) | 2026-09-16, 144 restaurants |
| Los Angeles: Beverly Hills area (Beverly Hills, Beverly Grove, western West Hollywood, Century City, Pico-Robertson) | [`la/index.html`](la/index.html) | 2026-10-09, 54 restaurants |

Open either `index.html` in a browser; everything (data, street basemap, app) is inline.

## LA run notes

- **Universe:** 193 restaurants and cafés mapped in OpenStreetMap in the study area (Overpass API). Every one with a website was attempted (the "OpenStreetMap census"), plus curated farm-forward and fine-dining picks.
- **Reading:** restaurant sites and menus were read with [Tavily](https://tavily.com) search/extract/crawl. Verbatim producer-naming sentences are kept as evidence. Spago's farms come from the menu it publishes to OpenTable, since its own page lists none.
- **Verification:** the USDA Organic INTEGRITY Database and CCOF directory could not be queried from this run, so no registry match was made. Organic claims (the farm's own, or an ORGANIC designation on the Santa Monica Farmers Market vendor list) are recorded as *leads*, never as a tier. As a result the grade ceiling for this run is C.
- **Result:** 7 C · 14 D · 33 E. 18 named producers (17 P4, 1 P5). Sites that failed to load, lapsed domains and closures are listed on the Findings page.
- `la/data.json` is the generated dataset; `la/pipeline/` holds the hand-curated evidence (`la_data.py`) and the build script, which uses the NYC page as its template.
