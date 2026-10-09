import json, collections
from la_data import *

# ---------------- restaurants ----------------
GRADE_REASON = {"D": "makes sourcing claims but names no producer", "E": "no sourcing disclosed (not yet asked)"}
BAND = {"most": 0.25, "some": 0.65, "claims": 1.0, "none": 1.0}
used = collections.defaultdict(list)

def base(rid, name, address, zp, cuisine, lat, lng, website, sample):
    return dict(sample=sample, camis=rid, name=name, address=address, zip=zp, cuisine=cuisine,
                neighborhood=NEIGHBORHOODS[zp], boro=CITY[zp], city=CITY[zp], lat=lat, lng=lng, website=website,
                verified_at=TODAY, season_note="", requests=[], last_crawled=TODAY, needs_js_render=False)

def detail(disclosure, produce_named=0, unconfirmed=(), opaque=()):
    return dict(disclosure=disclosure, declined=False, produce_named=produce_named, verified=0, verified_share=0.0,
                verified_names=[], lapsed=[], ambiguous=[], opaque_distributors=list(opaque), unconfirmed_alias=list(unconfirmed))

rs = []
for r in RESTAURANTS:
    o = base(r["id"], r["name"], r["address"], r["zip"], r["cuisine"], r["lat"], r["lng"], r["website"], r["sample"])
    sups = []
    for pid, raw, alias_ok, ctx, products, src in r["suppliers"]:
        p = PRODUCERS[pid]
        used[pid].append(r["id"])
        sups.append(dict(producer_id=pid, name=p[0], tier=p[5], type=p[1], category=p[2], flags=";".join(p[7]),
                         alias_confirmed=alias_ok, evidence=[dict(name_raw=raw, context=ctx, products=products, source_url=src, fetched_at=FETCHED)]))
    produce = [s for s in sups if s["category"] in ("produce", "unclear")]
    tiers = collections.Counter(s["tier"].split("-")[0] for s in produce)
    n = len(sups)
    o.update(grade="C", grade_reason=f"names {n} producer{'s' if n > 1 else ''}, none verified as organic or peer-certified yet",
             grade_detail=detail("some", len(produce), [s["name"] for s in sups if not s["alias_confirmed"]],
                                 [s["name"] for s in sups if s["tier"] == "P5-opaque"]),
             disclosure_mode="published", coverage="some", marketing_claims=r["claims"], sourcing_url=r["sourcing_url"],
             notes=r["notes"], profile=dict(named=len(produce), tiers=dict(tiers), undisclosed_band=BAND["some"], p1p2_share=0),
             badge_eligible=False, named_any=n, suppliers=sups, pages_archived=r["pages"])
    rs.append(o)

for grade, rows in (("D", D), ("E", E)):
    for rid, name, address, zp, cuisine, lat, lng, website, sample, note in rows:
        o = base(rid, name, address, zp, cuisine, lat, lng, website, sample)
        o.update(grade=grade, grade_reason=GRADE_REASON[grade], grade_detail=detail("claims" if grade == "D" else "none"),
                 disclosure_mode="unasked", coverage="none", marketing_claims=grade == "D", sourcing_url="",
                 notes=("Reviewed " + TODAY + ": " + note) if note else f"Reviewed {TODAY}: no sourcing claim or producer name found on the pages read.",
                 profile=dict(named=0, tiers={}, undisclosed_band=1.0, p1p2_share=0), badge_eligible=False, named_any=0,
                 suppliers=[], pages_archived=1)
        rs.append(o)

order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
rs.sort(key=lambda r: (order[r["grade"]], -r["named_any"], r["name"]))
assert len({r["camis"] for r in rs}) == len(rs)

# ---------------- producers ----------------
ps = []
for pid, p in PRODUCERS.items():
    name, typ, cat, city, state, tier, basis, flags, site, notes = p
    ps.append(dict(producer_id=pid, canonical_name=name, type=typ, category=cat, state=state, city=city, tier=tier, tier_basis=basis,
                   nop_op_id="", certifier="", op_status="", status_effective="", anniversary="", scopes_certified="", crops_products="",
                   integrity_checked="", alt_cert="", alt_cert_url="", alt_cert_checked="", questionnaire_date="", resolves_to="",
                   flags=flags, website=site, notes=notes, restaurants=used[pid], n_restaurants=len(used[pid])))
ps.sort(key=lambda p: (-p["n_restaurants"], p["canonical_name"]))

# ---------------- aggregate ----------------
links = sum(p["n_restaurants"] for p in ps)
top20 = sum(p["n_restaurants"] for p in ps[:20])
osm = [r for r in rs if r["sample"] == "osm"]
agg = dict(
    slice=" · ".join(SLICES), zips=[z for v in SLICES.values() for z in v],
    universe=193, with_website=len(rs) + len(NOT_CRAWLED), crawled=len(rs),
    disclosing=sum(1 for r in rs if r["named_any"]), disclosure_rate=round(sum(1 for r in rs if r["named_any"]) / len(rs), 3),
    grades=dict(collections.Counter(r["grade"] for r in rs)),
    producer_tiers=dict(collections.Counter(p["tier"].split("-")[0] for p in ps)),
    producers=len(ps), links=links, top20_share=round(top20 / links, 2),
    produce_disclosing=sum(1 for r in rs if r["profile"]["named"]),
    claims_only=sum(1 for r in rs if r["grade"] == "D"),
    organic_leads=sum(1 for p in ps if {"sm-market-organic", "self-declared-organic"} & set(p["flags"])),
    not_crawled=[dict(camis="", name=n, reason=why) for n, why in NOT_CRAWLED],
    closed=[dict(name=n, reason=why) for n, why in CLOSED],
    random_sample=dict(n=len(osm), disclosing=sum(1 for r in osm if r["named_any"])),
    kill_threshold=0.15)

DATA = dict(generated_at=TODAY + "T16:00:00Z", integrity_snapshot="not queried",
            neighborhoods=NEIGHBORHOODS, slices=SLICES, contact="indiaclarke03@gmail.com",
            non_response_rule="3 attempts across 2 channels over 30 days",
            badge_rule="Grade A and at least 80% of named produce suppliers at P1/P2",
            aggregate=agg, restaurants=rs, producers=ps)

# ---------------- basemap ----------------
osmb = json.load(open("osm_base.json"))
CLS = {"primary": "major", "trunk": "major", "motorway": "major", "secondary": "mid", "tertiary": "mid"}
roads, water, parks = [], [], []
r5 = lambda g: [[round(pt["lat"], 5), round(pt["lon"], 5)] for pt in g]
for e in osmb["elements"]:
    t, g = e["tags"], e.get("geometry")
    if not g: continue
    if "highway" in t: roads.append(dict(c=CLS.get(t["highway"], "minor"), n=t.get("name", ""), p=r5(g)))
    elif t.get("natural") == "water": water.append(r5(g))
    elif t.get("leisure") in ("park", "golf_course"): parks.append(r5(g))
BASEMAP = dict(bbox=[34.050, -118.425, 34.095, -118.365], roads=roads, water=water, parks=parks)

# ---------------- page ----------------
L = open("nyc.html").read().split("\n")
assert L[206].startswith("window.PROVENANCE_DATA") and L[210].startswith("window.PROVENANCE_BRAND") and L[214].startswith("window.PROVENANCE_BASEMAP")
L[0] = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
L[206] = "window.PROVENANCE_DATA = " + json.dumps(DATA, ensure_ascii=False) + ";"
L[210] = "window.PROVENANCE_BRAND=" + json.dumps({r["camis"]: {"display_name": r["name"]} for r in rs}, ensure_ascii=False) + ";"
L[214] = "window.PROVENANCE_BASEMAP=" + json.dumps(BASEMAP, separators=(",", ":")) + ";"
html = "\n".join(L)

def sub(old, new, count=1):
    global html
    n = html.count(old)
    assert n == count, (n, old[:80])
    html = html.replace(old, new)

sub("<title>Provenance NYC</title>", "<title>Provenance LA</title>")
sub("/* Provenance NYC — design tokens.", "/* Provenance LA — design tokens.")
sub('<span class="beta">NYC · beta</span>', '<span class="beta">LA · beta</span>')
sub("/* Provenance NYC — static front end.", "/* Provenance LA — static front end.")
sub("`Data generated ${(D.generated_at || '').slice(0,10)} · USDA INTEGRITY snapshot ${D.integrity_snapshot || ''} · ",
    "`Data generated ${(D.generated_at || '').slice(0,10)} · Read with Tavily · Map data © OpenStreetMap contributors · USDA INTEGRITY: ${D.integrity_snapshot || ''} · ")
sub("setView([40.722, -73.975], 13)", "setView([34.07, -118.395], 14)")
sub("Sourcing transparency · New York City", "Sourcing transparency · Beverly Hills area, Los Angeles")
sub("We read restaurants' own websites for the farms they name, check every named producer against the USDA Organic INTEGRITY Database and five peer-certification directories, and grade each restaurant",
    "We read restaurants' own websites and menus for the farms they name, check every named producer for a certification record and against the organic designations in the Santa Monica and Beverly Hills farmers' market registries, and grade each restaurant")
sub("permitted establishments across ${Object.keys(D.slices || {}).length} contiguous areas (DOHMH)",
    "restaurants and cafés mapped in OpenStreetMap across ${Object.keys(D.slices || {}).length} contiguous areas")
sub("restaurant websites crawled and graded so far", "restaurant websites read and graded so far")
sub("in the random sample</span>", "in the OpenStreetMap census</span>")
sub("${a.producer_tiers?.P4 || 0} awaiting verification", "${a.producer_tiers?.P4 || 0} awaiting verification · ${a.organic_leads || 0} carry organic leads")
sub("<div><b>1 · Read</b>We crawl each restaurant's own site — menus, about and purveyor pages, PDF menus — and keep the exact sentence that names a farm.</div>",
    "<div><b>1 · Read</b>We read each restaurant's own site and the menu it publishes — menus, about and purveyor pages — and keep the exact sentence that names a farm.</div>")
sub("<div><b>2 · Verify</b>Every named producer is looked up in the USDA Organic INTEGRITY Database (a federal registry) and the Certified Naturally Grown directory.</div>",
    "<div><b>2 · Verify</b>Every named producer is looked up for a certification record (USDA Organic INTEGRITY, CCOF) and in the Santa Monica and Beverly Hills farmers' market vendor lists. A market's “organic” label is a lead to confirm, never a tier.</div>")
sub("Only crawled restaurants appear; the rest of the ${a.universe?.toLocaleString()} permitted establishments are queued.",
    "Only restaurants whose sites were read appear; the rest of the ${a.universe?.toLocaleString()} mapped establishments are queued.")
sub("mail('Provenance NYC feedback'", "mail('Provenance LA feedback'")
sub("${r.sample === 'random' ? ' · random sample' : ''}", "${r.sample === 'osm' ? ' · OpenStreetMap census' : ''}")
sub("${esc(title(r.address))}, ${r.boro === 'Brooklyn' ? 'Brooklyn' : 'New York'} ${esc(r.zip)}", "${esc(r.address)}, ${esc(r.city || 'Los Angeles')}, CA ${esc(r.zip)}")
sub("${r.pages_archived} page(s) archived with timestamps and hashes.", "${r.pages_archived} page(s) read with Tavily on ${esc(r.last_crawled)}.")
sub("'registry-ambiguous':'Two registry records; not matched on name alone'}",
    "'registry-ambiguous':'Common name; not matched on name alone','sm-market-organic':'Santa Monica Farmers Market lists as ORGANIC (lead)','sm-market-vendor':'Sells at Santa Monica Farmers Market','bh-market-vendor':'Sells at Beverly Hills Farmers Market','self-declared-organic':'Farm site says certified organic (lead)','certified-humane':'Certified Humane (welfare, not organic)'}")
sub("Specialty distributors serving NYC carry substantial organic and regional product; this tier is not a quality signal on its own.",
    "A brand program or specialty distributor can carry good product; this tier is not a quality signal on its own.")
sub("Producers named by New York restaurants", "Producers named by Beverly Hills-area restaurants")

# findings page: LA-specific prose
f0 = html.index("function findings(){")
f1 = html.index("function method(){")
FINDINGS = r"""function findings(){
  const a = D.aggregate, g = a.grades || {}, t = a.producer_tiers || {};
  const gradeColors = {A:'var(--gA)', B:'var(--gB)', C:'var(--gC)', D:'var(--gD)', E:'var(--gE)'}, tierColors = {P1:'var(--p1)', P2:'var(--p2)', P3:'var(--p3)', P4:'var(--p4)', P5:'var(--p5)'};
  const byHood = {}; D.restaurants.forEach(r => { const h = byHood[r.neighborhood] = byHood[r.neighborhood] || {n:0, d:0}; h.n++; if (r.named_any) h.d++; });
  const hoodRows = Object.entries(byHood).sort((x, y) => y[1].n - x[1].n).map(([h, v]) => [h, v.d, 'x', v.n]);
  const top = D.producers.slice(0, 10);
  const leads = D.producers.filter(p => p.flags.includes('sm-market-organic') || p.flags.includes('self-declared-organic'));
  app.innerHTML = `<div class="prose"><div class="eyebrow">What we found</div><h1>Beverly Hills says “local” and “organic” far more often than it says who.</h1>
  <p class="lede" style="color:var(--ink-2)">Seed run, ${esc((D.generated_at || '').slice(0,10))}. ${a.crawled} restaurant websites read across ${Object.keys(D.slices || {}).length} contiguous areas: Beverly Hills, Beverly Grove and western West Hollywood, Century City and Pico-Robertson. <strong>${a.disclosing}</strong> name at least one food producer (${Math.round((a.disclosure_rate || 0)*100)}%). <strong>${a.produce_disclosing}</strong> name a produce supplier. <strong>${a.claims_only}</strong> make “local”, “organic” or “farm” claims without naming anyone. Of the ${a.random_sample?.n || 0} restaurants drawn from the OpenStreetMap census rather than picked for their reputation, <strong>${a.random_sample?.disclosing || 0}</strong> named a producer, and both of those name beef brands.</p>
  <h2>Transparency grades</h2>${barChart(['A','B','C','D','E'].map(k => [`${k} · ${GRADE_SHORT[k]}`, g[k] || 0, k]), gradeColors)}
  <p class="sub">No restaurant earns an A or B yet. A B needs at least one named produce supplier with a confirmed certification record, and none could be confirmed in this run (see below). The Cs are real disclosure: Spago's menu names five farms, A.O.C. names three growers by name or first name, and Farmhouse is owned by a farmer.</p>
  <h2>What verification exists for the ${a.producers} named producers</h2>${barChart(['P1','P2','P3','P5','P4'].filter(k => t[k]).map(k => [`${k} · ${TIER_SHORT[k]}`, t[k], k]), tierColors)}
  <p class="sub">Every named producer is P4 (named, not yet verified) except one beef brand program. That is partly a data-access result: the USDA Organic INTEGRITY Database and the CCOF directory are interactive apps that could not be queried from this run, so no registry match was made. <strong>${leads.length} named farms carry organic leads</strong> (${leads.map(p => `<a href="#/p/${p.producer_id}">${esc(p.canonical_name)}</a>`).join(', ')}): the farm says it is certified, or the Santa Monica Farmers Market lists it as ORGANIC. Under our rules a lead is never a tier. Confirming those records is the first job of the next pass, and would move Spago to B.</p>
  <h2>Disclosure by neighborhood</h2>${barChart(hoodRows.map(([h, d, c, n]) => [`${h.length > 26 ? h.slice(0, 24) + '…' : h} (${d}/${n})`, d, c]), {x: 'var(--accent)'})}
  <p class="sub">Bars show restaurants naming at least one producer; the bracket is restaurants read in that area. Curated picks over-represent known farm-forward kitchens; the OpenStreetMap census is the honest read.</p>
  <h2>Most-named producers</h2><div class="panel tablewrap"><table><tr><th>Producer</th><th>Tier</th><th>Named by</th></tr>${top.map(p => `<tr><td><a href="#/p/${p.producer_id}">${esc(p.canonical_name)}</a> <span class="sub">${esc([p.city, p.state].filter(Boolean).join(', '))}</span></td><td><span class="chip tier ${tierBase(p.tier)}">${esc(p.tier)}</span></td><td>${p.n_restaurants}</td></tr>`).join('')}</table></div>
  <p>Weiser Family Farms is the only producer named by two restaurants. Several of the named farms sell at the Santa Monica and Beverly Hills farmers' markets, the same markets a Beverly Hills diner can walk to on Sunday.</p>
  <h2>Not yet graded</h2><p class="sub">These sites failed to load, returned an error, or the domain has lapsed to unrelated content. They are queued, not graded.</p><ul>${(a.not_crawled || []).map(x => `<li>${esc(x.name)} <span class="sub">(${esc(x.reason)})</span></li>`).join('')}</ul>
  <h2>Closed</h2><p class="sub">Found closed during the run and left out.</p><ul>${(a.closed || []).map(x => `<li>${esc(x.name)} <span class="sub">(${esc(x.reason)})</span></li>`).join('')}</ul>
  <h2>How this was made</h2><p>Restaurant universe from OpenStreetMap: every restaurant and café mapped in the study area (${a.universe}), via the Overpass API. Curated picks were added for known farm-forward and fine-dining kitchens. Each restaurant's own site and menu pages were read with Tavily (search, extract and crawl) on ${esc((D.generated_at || '').slice(0,10))}, keeping the verbatim sentence that names a producer. Spago's farms come from the dinner menu it publishes to OpenTable, because its own page lists none. Producers were checked with Tavily against their own sites, certifier pages and the City of Santa Monica and City of Beverly Hills farmers' market vendor lists, matched on name plus place, never name alone. Street map © OpenStreetMap contributors.</p></div>`;
}
"""
html = html[:f0] + FINDINGS + html[f1:]

sub("<p><strong>Context registries.</strong> Two more sources add context without changing a tier: GrowNYC's own description of each Greenmarket producer (a “Certified Organic” description there is a lead we confirm in INTEGRITY, never a tier by itself) and the A Greener World directory (livestock-welfare programs, not a produce certification). Both appear as flags and notes on producer pages.</p>",
    "<p><strong>Context registries.</strong> Two sources add context without changing a tier: the City of Santa Monica Farmers Market vendor list, which marks some vendors ORGANIC, and the City of Beverly Hills Farmers' Market vendor list. A market's “organic” label, like a farm's own claim to be certified, is a lead we confirm in INTEGRITY, never a tier by itself. Welfare programs such as Certified Humane are shown as flags, not as an organic certification.</p><p><strong>This run.</strong> The USDA Organic INTEGRITY Database and the CCOF member directory are interactive applications that could not be queried from the seed run, so no producer has been matched to a registry record yet. Every organic claim is therefore held as a lead, and the grade ceiling for every restaurant in this run is C.</p>")

open("provenance-la.html", "w").write(html)
json.dump(DATA, open("la_data.json", "w"), ensure_ascii=False, indent=1)
print(len(rs), agg["grades"], agg["producer_tiers"], agg["random_sample"], "html bytes", len(html))
