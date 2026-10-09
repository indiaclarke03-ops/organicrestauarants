import json, collections
from la_data import *
import la_pass2 as P2

# ---------------- producers (pass 1 + pass 2 overrides) ----------------
PROD = {}
for pid, p in PRODUCERS.items():
    name, typ, cat, city, state, tier, basis, flags, site, notes = p
    PROD[pid] = dict(producer_id=pid, canonical_name=name, type=typ, category=cat, state=state, city=city, tier=tier, tier_basis=basis,
                     nop_op_id="", certifier="", op_status="", status_effective="", anniversary="", scopes_certified="", crops_products="",
                     integrity_checked="", alt_cert="", alt_cert_url="", alt_cert_checked="", questionnaire_date="", resolves_to="",
                     flags=list(flags), website=site, notes=notes, judgement=[])
for pid, p in P2.NEW_PRODUCERS.items():
    name, typ, cat, city, state, tier, basis, flags, site, notes, judg = p
    PROD[pid] = dict(PROD["L001"], producer_id=pid, canonical_name=name, type=typ, category=cat, state=state, city=city, tier=tier,
                     tier_basis=basis, flags=list(flags), website=site, notes=notes, judgement=[])
    PROD[pid]["judgement"] = [dict(source=a, url=b, says=c) for a, b, c in judg]
for pid, o in P2.OVERRIDES.items():
    o = dict(o)
    PROD[pid]["flags"] += o.pop("flags_add", [])
    if "judgement" in o: o["judgement"] = [dict(source=a, url=b, says=c) for a, b, c in o["judgement"]]
    PROD[pid].update(o)
VERIFIED = ("P1", "P2", "P3")
tb = lambda t: t.split("-")[0]

# ---------------- restaurants ----------------
GRADE_REASON = {"D": "makes sourcing claims but names no producer", "E": "no sourcing disclosed (not yet asked)"}
BAND = {"most": 0.25, "some": 0.65, "claims": 1.0, "none": 1.0}
used = collections.defaultdict(list)

def base(rid, name, address, zp, cuisine, lat, lng, website, sample):
    return dict(sample=sample, camis=rid, name=name, address=address, zip=zp, cuisine=cuisine,
                neighborhood=NEIGHBORHOODS[zp], boro=CITY[zp], city=CITY[zp], lat=lat, lng=lng, website=website,
                verified_at=TODAY, season_note="", requests=[], last_crawled=TODAY, needs_js_render=False)

rs = []
for r in RESTAURANTS + P2.NEW_C:
    o = base(r["id"], r["name"], r["address"], r["zip"], r["cuisine"], r["lat"], r["lng"], r["website"], r["sample"])
    o["season_note"] = r.get("season_note", "")
    sups = []
    for pid, raw, alias_ok, ctx, products, src in r["suppliers"]:
        p = PROD[pid]
        alias_note = P2.ALIAS_CONFIRM.get((r["id"], pid))
        if alias_note: alias_ok = True
        used[pid].append(r["id"])
        sups.append(dict(producer_id=pid, name=p["canonical_name"], tier=p["tier"], type=p["type"], category=p["category"], flags=";".join(p["flags"]),
                         alias_confirmed=alias_ok, alias_note=alias_note or "",
                         evidence=[dict(name_raw=raw, context=ctx, products=products, source_url=src, fetched_at=FETCHED)]))
    produce = [s for s in sups if s["category"] in ("produce", "unclear")]
    ver = [s for s in produce if tb(s["tier"]) in VERIFIED and s["alias_confirmed"]]
    tiers = collections.Counter(tb(s["tier"]) for s in produce)
    n, share = len(sups), (len(ver) / len(produce) if produce else 0.0)
    disclosure = "some"
    if ver:
        grade = "A" if disclosure == "most" and share >= 0.5 else "B"
        reason = f"{len(ver)} of {len(produce)} named produce suppliers verified or judged organic ({round(share*100)}%); " + \
                 ("producers not yet named for most of the menu" if disclosure != "most" else "A needs at least half")
    else:
        grade, reason = "C", f"names {n} producer{'s' if n > 1 else ''}, none verified or judged organic yet"
    unconf = [s["name"] for s in sups if not s["alias_confirmed"]]
    o.update(grade=grade, grade_reason=reason,
             grade_detail=dict(disclosure=disclosure, declined=False, produce_named=len(produce), verified=len(ver), verified_share=round(share, 2),
                               verified_names=[s["name"] for s in ver], lapsed=[], ambiguous=[],
                               opaque_distributors=[s["name"] for s in sups if s["tier"] == "P5-opaque"], unconfirmed_alias=unconf),
             disclosure_mode="published", coverage=disclosure, marketing_claims=r["claims"], sourcing_url=r["sourcing_url"],
             notes=r["notes"] + "".join(" Alias confirmed: " + s["alias_note"] for s in sups if s["alias_note"]),
             profile=dict(named=len(produce), tiers=dict(tiers), undisclosed_band=BAND[disclosure], p1p2_share=round(share, 2)),
             badge_eligible=False, named_any=n, suppliers=sups, pages_archived=r["pages"])
    rs.append(o)

for grade, rows in (("D", D), ("E", E)):
    for rid, name, address, zp, cuisine, lat, lng, website, sample, note in rows:
        if rid in P2.REMOVE_FROM_DE: continue
        o = base(rid, name, address, zp, cuisine, lat, lng, website, sample)
        o.update(grade=grade, grade_reason=GRADE_REASON[grade],
                 grade_detail=dict(disclosure="claims" if grade == "D" else "none", declined=False, produce_named=0, verified=0, verified_share=0.0,
                                   verified_names=[], lapsed=[], ambiguous=[], opaque_distributors=[], unconfirmed_alias=[]),
                 disclosure_mode="unasked", coverage="none", marketing_claims=grade == "D", sourcing_url="",
                 notes=("Reviewed " + TODAY + ": " + note) if note else f"Reviewed {TODAY}: no sourcing claim or producer name found on the pages read.",
                 profile=dict(named=0, tiers={}, undisclosed_band=1.0, p1p2_share=0), badge_eligible=False, named_any=0,
                 suppliers=[], pages_archived=1)
        rs.append(o)

order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
rs.sort(key=lambda r: (order[r["grade"]], -r["grade_detail"]["verified"], -r["named_any"], r["name"]))
assert len({r["camis"] for r in rs}) == len(rs)

ps = []
for pid, p in PROD.items():
    if not used[pid]: continue
    ps.append(dict(p, restaurants=used[pid], n_restaurants=len(used[pid])))
ps.sort(key=lambda p: (-p["n_restaurants"], ["P1","P2","P3","P5","P4"].index(tb(p["tier"])), p["canonical_name"]))

# ---------------- aggregate ----------------
links = sum(p["n_restaurants"] for p in ps)
top20 = sum(p["n_restaurants"] for p in ps[:20])
osm = [r for r in rs if r["sample"] == "osm"]
NOT_CRAWLED2 = NOT_CRAWLED + P2.NEW_NOT_CRAWLED[:1]
agg = dict(
    slice=" · ".join(SLICES), zips=[z for v in SLICES.values() for z in v],
    universe=193, with_website=len(rs) + len(NOT_CRAWLED2), crawled=len(rs),
    disclosing=sum(1 for r in rs if r["named_any"]), disclosure_rate=round(sum(1 for r in rs if r["named_any"]) / len(rs), 3),
    grades=dict(collections.Counter(r["grade"] for r in rs)),
    producer_tiers=dict(collections.Counter(tb(p["tier"]) for p in ps)),
    producers=len(ps), links=links, top20_share=round(top20 / links, 2),
    produce_disclosing=sum(1 for r in rs if r["profile"]["named"]),
    claims_only=sum(1 for r in rs if r["grade"] == "D"),
    produce_verified=sum(1 for p in ps if p["category"] == "produce" and tb(p["tier"]) in VERIFIED),
    not_crawled=[dict(camis="", name=n, reason=why) for n, why in NOT_CRAWLED2],
    closed=[dict(name=n, reason=why) for n, why in CLOSED + P2.NEW_CLOSED],
    random_sample=dict(n=len(osm), disclosing=sum(1 for r in osm if r["named_any"])),
    kill_threshold=0.15)

DATA = dict(generated_at=TODAY + "T16:00:00Z", integrity_snapshot="not queried; CCOF directory checked " + P2.CHECKED,
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
  const top = D.producers.slice(0, 12);
  const link = p => `<a href="#/p/${p.producer_id}">${esc(p.canonical_name)}</a>`;
  const ver = D.producers.filter(p => p.category === 'produce' && ['P1','P2','P3'].includes(tierBase(p.tier)));
  const bs = D.restaurants.filter(r => r.grade === 'B' || r.grade === 'A');
  app.innerHTML = `<div class="prose"><div class="eyebrow">What we found</div><h1>Beverly Hills says “local” and “organic” far more often than it says who.</h1>
  <p class="lede" style="color:var(--ink-2)">Two passes, ${esc((D.generated_at || '').slice(0,10))}. ${a.crawled} restaurants read across ${Object.keys(D.slices || {}).length} contiguous areas: Beverly Hills, Beverly Grove and western West Hollywood, Century City and Pico-Robertson. <strong>${a.disclosing}</strong> name at least one food producer (${Math.round((a.disclosure_rate || 0)*100)}%), but only <strong>${a.produce_disclosing}</strong> name a produce grower. <strong>${a.claims_only}</strong> make “local”, “organic” or “farm” claims without naming anyone. Of the ${a.random_sample?.n || 0} restaurants drawn from the OpenStreetMap census rather than picked for their reputation, <strong>${a.random_sample?.disclosing || 0}</strong> named a producer.</p>
  <h2>Who can show organic produce</h2>
  <p>${bs.length ? `<strong>${bs.length} restaurant${bs.length > 1 ? 's' : ''}</strong> earn a B: ${bs.map(r => `<a href="#/r/${r.camis}">${esc(dname(r))}</a> (${r.grade_detail.verified} of ${r.grade_detail.produce_named} named produce growers verified or judged organic)`).join('; ')}.` : 'No restaurant earns a B yet.'} None earns an A, because none names growers for most of its menu. Spago's menu names five farms and four of them check out; Farmhouse is owned by a farmer whose family farm is judged organic.</p>
  <h2>Transparency grades</h2>${barChart(['A','B','C','D','E'].map(k => [`${k} · ${GRADE_SHORT[k]}`, g[k] || 0, k]), gradeColors)}
  <p class="sub">Most Cs name beef, cheese or bread brands rather than produce growers. Steakhouses are the most forthcoming about where their meat comes from and the least about their vegetables.</p>
  <h2>What verification exists for the ${a.producers} named producers</h2>${barChart(['P1','P2','P3','P5','P4'].filter(k => t[k]).map(k => [`${k} · ${TIER_SHORT[k]}`, t[k], k]), tierColors)}
  <p class="sub"><strong>Registry-verified:</strong> ${D.producers.filter(p => tierBase(p.tier) === 'P1').map(link).join(', ') || 'none'} (CCOF lists it as certified organic since 1997). <strong>Judged organic</strong> on reasonable evidence: ${D.producers.filter(p => tierBase(p.tier) === 'P3').map(link).join(', ')}. Three of those (See Canyon, Polito, Munak) are uncertified farms whose buyers describe them as farming without synthetic pesticides. <strong>Not organic on the evidence:</strong> Zuckerman's Farm is listed as conventional by its distributor, and Weiser Family Farms describes itself as sustainable, not organic. Each producer page shows the sources behind its tier.</p>
  <h2>Disclosure by neighborhood</h2>${barChart(hoodRows.map(([h, d, c, n]) => [`${h.length > 26 ? h.slice(0, 24) + '…' : h} (${d}/${n})`, d, c]), {x: 'var(--accent)'})}
  <p class="sub">Bars show restaurants naming at least one producer; the bracket is restaurants read in that area. Curated picks over-represent known farm-forward kitchens; the OpenStreetMap census is the honest read.</p>
  <h2>Named producers</h2><div class="panel tablewrap"><table><tr><th>Producer</th><th>Tier</th><th>Named by</th></tr>${top.map(p => `<tr><td>${link(p)} <span class="sub">${esc([p.city, p.state].filter(Boolean).join(', '))}</span></td><td><span class="chip tier ${tierBase(p.tier)}">${esc(p.tier)}</span></td><td>${p.n_restaurants}</td></tr>`).join('')}</table></div>
  <p><a href="#/producers">All ${a.producers} producers →</a></p>
  <h2>Not yet graded</h2><p class="sub">These sites failed to load, returned an error, or the domain has lapsed to unrelated content. They are queued, not graded.</p><ul>${(a.not_crawled || []).map(x => `<li>${esc(x.name)} <span class="sub">(${esc(x.reason)})</span></li>`).join('')}</ul>
  <h2>Closed</h2><p class="sub">Found closed during the run and left out.</p><ul>${(a.closed || []).map(x => `<li>${esc(x.name)} <span class="sub">(${esc(x.reason)})</span></li>`).join('')}</ul>
  <h2>How this was made</h2><p>Restaurant universe from OpenStreetMap: every restaurant and café mapped in the study area (${a.universe}), via the Overpass API, plus curated farm-forward, hotel and fine-dining picks. Pass 1 read each restaurant's own site; pass 2 went back for the actual menus (PDFs, menu pages, the menu a restaurant publishes to OpenTable, and its own social posts) using Tavily search, extract and crawl, keeping the verbatim sentence that names a producer. Producers were then checked against the CCOF certified-member directory, farm websites, distributor and buyer profiles, and the City of Santa Monica and City of Beverly Hills farmers' market vendor lists, matched on name plus place. Street map © OpenStreetMap contributors.</p></div>`;
}
"""
html = html[:f0] + FINDINGS + html[f1:]

sub("<p><strong>Context registries.</strong> Two more sources add context without changing a tier: GrowNYC's own description of each Greenmarket producer (a “Certified Organic” description there is a lead we confirm in INTEGRITY, never a tier by itself) and the A Greener World directory (livestock-welfare programs, not a produce certification). Both appear as flags and notes on producer pages.</p>",
    "<p><strong>Context registries.</strong> The City of Santa Monica Farmers Market vendor list (which marks certified vendors ORGANIC) and the City of Beverly Hills Farmers' Market vendor list. Welfare programs such as Certified Humane are shown as flags, not as an organic certification.</p><p><strong>Reasonable judgement (P3).</strong> A registry record is the strongest evidence, but small farms are often organic in practice without a certificate, and the USDA INTEGRITY database could not be queried from this run. So a farm is <em>judged organic</em> when (a) the farm itself, or a buyer, distributor or market that deals with it, says it is organic or farms without synthetic pesticides and fertilisers, and (b) no record contradicts that, such as a distributor listing it as conventional. Every source is quoted on the producer page, and uncertified farms are flagged as such. Judged-organic growers count toward a restaurant's grade the same as certified ones. Name matches follow the same standard: a first name or description counts once independent sources tie it to one farm.</p>")


sub("P3:'Documented practices', P4", "P3:'Judged organic (reasonable evidence)', P4")
sub("P3:'Documented', P4", "P3:'Judged organic', P4")
sub("B:'Names verified organic or peer-certified producers'", "B:'Names verified or judged-organic producers'")
sub("P3 documented</span>", "P3 judged organic</span>")
sub("how much of it is verified organic or peer-certified, and whether", "how much of it is verified or judged organic, and whether")
sub("verified organic or peer-certified (${Math.round(d.verified_share * 1", "verified or judged organic (${Math.round(d.verified_share * 1")
sub("<td>Documented practices, self-declared</td><td>A signed, dated questionnaire with yes/no answers (synthetic pesticides, synthetic fertiliser, GMO seed, soil vs hydroponic, transition status). Marketing language does not qualify. Expires after 12 months.</td>",
    "<td>Judged organic on reasonable evidence</td><td>The farm, or a buyer, distributor or market that deals with it, says it is organic or farms without synthetic pesticides and fertilisers, and nothing on record contradicts it. Every source is quoted. Uncertified farms are flagged. A signed practices questionnaire also qualifies. Re-checked every 12 months.</td>")
sub("(P1 USDA-certified or P2 peer-certified produce suppliers)", "(P1 registry-certified, P2 peer-certified or P3 judged-organic produce suppliers)")
sub("At least one named produce supplier is USDA-certified or peer-certified.", "At least one named produce supplier is certified, peer-certified or judged organic on reasonable evidence.")
sub("<h3>C → B</h3><p>At least one named produce supplier must hold a current USDA organic certification or a peer certification (CNG, Real Organic Project, ROC, Demeter). Point us to the registry record and we match it.</p>",
    "<h3>C → B</h3><p>At least one named produce supplier must be certified organic, peer-certified, or shown on reasonable evidence to farm organically. Point us to a registry record, or to the farm's own statement of its practices, and we check it.</p>")
sub("<h3>P4 → P3</h3><p>Answer a short practices questionnaire,", "<h3>P4 → P3</h3><p>Show us a public statement of your practices that a buyer or market can corroborate, or answer a short practices questionnaire,")
sub("A farm can move to P3 with a signed practices questionnaire, or to P1/P2 by poi", "A farm can move to P3 by showing it farms organically, or to P1/P2 by poi")
sub("'certified-humane':'Certified Humane (welfare, not organic)'}", "'certified-humane':'Certified Humane (welfare, not organic)','uncertified-organic-practices':'Organic practices, not certified','documented-conventional':'Listed as conventional by its distributor'}")
sub("${a.producer_tiers?.P4 || 0} awaiting verification · ${a.organic_leads || 0} carry organic leads", "${a.producer_tiers?.P1 || 0} certified · ${a.producer_tiers?.P3 || 0} judged organic · ${a.producer_tiers?.P4 || 0} awaiting verification")
sub("${a.producer_tiers?.P1 || 0} USDA-certified · ${a.producer_tiers?.P2 || 0} peer-certified · ", "")
sub("A market's “organic” label is a lead to confirm, never a tier.</div>", "Where no certificate exists, a farm can be judged organic on corroborated evidence of its practices.</div>")
sub("     <dt>Scopes</dt><dd>${esc((p.scopes_certified || '').replace(/;/g, ' · '))}</dd><dt>Certified products (Crops)</dt><dd>${esc(p.crops_products || '—')}</dd><dt>Checked against snapshot</dt><dd>${esc(p.integrity_checked)}</dd></dl>` : '';",
    "     <dt>Scopes</dt><dd>${esc((p.scopes_certified || '').replace(/;/g, ' · '))}</dd><dt>Certified products (Crops)</dt><dd>${esc(p.crops_products || '—')}</dd><dt>Checked against snapshot</dt><dd>${esc(p.integrity_checked)}</dd></dl>` : (p.certifier ? `<dl class=\"kv\"><dt>Certifier</dt><dd>${esc(p.certifier)}</dd><dt>Status</dt><dd>${esc(p.op_status)} (since ${esc(p.status_effective)})</dd><dt>Scopes</dt><dd>${esc((p.scopes_certified || '').replace(/;/g, ' · '))}</dd><dt>Record</dt><dd><a href=\"${esc(p.alt_cert_url)}\" target=\"_blank\" rel=\"noopener\">${esc(p.alt_cert_url)}</a></dd><dt>Checked</dt><dd>${esc(p.integrity_checked)}</dd></dl>` : '');\n  const judg = (p.judgement || []).length ? `<div class=\"eyebrow\" style=\"margin-top:14px\">Evidence behind this tier</div>${p.judgement.map(j => `<blockquote>${esc(j.says)}</blockquote><div class=\"sub\">${esc(j.source)} · <a href=\"${esc(j.url)}\" target=\"_blank\" rel=\"noopener\">source</a></div>`).join('')}` : '';")
sub("<p>${esc(p.tier_basis)}.</p>${ev}${alt}", "<p>${esc(p.tier_basis)}.</p>${ev}${alt}${judg}")

sub("Record in the USDA Organic INTEGRITY Database, status Certified", "Record in the USDA Organic INTEGRITY Database or the accredited certifier's own member directory (e.g. CCOF), status Certified")
open("provenance-la.html", "w").write(html)
json.dump(DATA, open("la_data.json", "w"), ensure_ascii=False, indent=1)
print(len(rs), agg["grades"], agg["producer_tiers"], agg["random_sample"], "html bytes", len(html))
