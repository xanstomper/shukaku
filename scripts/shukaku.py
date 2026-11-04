#!/usr/bin/env python3
"""
SHUKAKU — Harvest Mandate CLI. Reason · hunt · crown · price · disclose · feed.
stdlib-only. State: ~/.redteam/campaigns/<campaign>/harvest-state.json.

The harvester doesn't just price what it's told about — it REASONS about what
should be harvestable from confirmed access, HUNTS for it (read-only), and FEEDS
every discovery back to the family so the next assault is stronger.

Commands:
  ingest    --target <c> --finding "<id>" --proof "<read-only proof ref>"
  reason    --target <c> [--json]     infer harvestable planes from confirmed access
  hunt      --target <c> [--live URL] [--cookie k=v] [--dry-run] [--max N]
                                      work the hypotheses: exact read-only proofs
                                      (static) or GET-only live harvest-surface probes
  crown     --target <c> --asset "<table|bucket|export>" --class PII|FIN|CRED|BACKUP|SRC|SASS
            --scope "<counts, not contents>" --source "<ingested finding ID>"
            [--value "$ESTIMATE"] [--basis "..."]
  exclude   --target <c> --finding "<id>" --reason "no data reach | out of scope | wall"
  disclose  --target <c> --trigger PII-US|PII-EU|FIN|HEALTH|CONTRACT|RANSOM [--note "..."]
            [--add "<obligation> · <timeline> · <prerequisite>"]
  feed      --target <c>             harvest → family: 3AM vectors, undercroft seams,
                                     holyshit recipes (kairo ingests them next)
  ladder    [--class C]              the valuation ladder + disclosure map
  report    --target <c> [--output F]
  verify    self-check

Exit codes: 0 ok · 1 verify failure · 2 usage/state error.
"""
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CLASSES = ("PII", "FIN", "CRED", "BACKUP", "SRC", "SASS")

# The extortion-economy valuation ladder (references/harvest-playbook.md §Phase 2).
# Every price is an ESTIMATE range with a basis — a single-number price without
# basis is a violation.
LADDER = {
    "PII": [
        {"market": "PII — US consumer", "unit": "per 1k rows",
         "range": "$5,000–15,000 ESTIMATE",
         "basis": "~$5–15/record street; breach-class aggregation multipliers apply"},
        {"market": "PII — EU (GDPR-class)", "unit": "per 1k rows",
         "range": "lower street, higher penalty-weight ESTIMATE",
         "basis": "GDPR penalty economics shift value from resale to liability"},
    ],
    "FIN": [
        {"market": "FIN — cards/banking", "unit": "per record",
         "range": "$20–50 ESTIMATE", "basis": "financial-record class"},
    ],
    "CRED": [
        {"market": "CRED — secrets/keys", "unit": "per credential",
         "range": "tiered by privilege ESTIMATE",
         "basis": "credential-market tiers; keys and top-privilege secrets price highest"},
    ],
    "BACKUP": [
        {"market": "BACKUP — unencrypted dump", "unit": "per artifact",
         "range": "% of org revenue-class ESTIMATE",
         "basis": "ransom-demand logic on bulk artifacts"},
    ],
    "SRC": [
        {"market": "SRC — exclusive repo", "unit": "per repo",
         "range": "private-repo market + IP class ESTIMATE",
         "basis": "exclusive source market"},
    ],
    "SASS": [
        {"market": "SASS — tenant export", "unit": "per tenant",
         "range": "resale/takeover ladder ESTIMATE",
         "basis": "SaaS export market"},
    ],
}

# The disclosure map (references/harvest-playbook.md §Phase 3) — a DELIVERABLE
# for the operator's own org, never a threat.
DISCLOSURE = [
    {"trigger": "PII-US",   "obligation": "state AG notification laws",
     "timeline": "30d class",     "prerequisite": "investigation complete"},
    {"trigger": "PII-EU",   "obligation": "GDPR Art. 33/34",
     "timeline": "72h class",     "prerequisite": "risk assessment"},
    {"trigger": "FIN",      "obligation": "card brands + acquiring bank",
     "timeline": "immediate class", "prerequisite": "forensic report"},
    {"trigger": "HEALTH",   "obligation": "HIPAA/HITECH — HHS",
     "timeline": "60d class",     "prerequisite": "risk assessment"},
    {"trigger": "CONTRACT", "obligation": "contracts/insurance breach clauses",
     "timeline": "policy class",  "prerequisite": "legal review"},
    {"trigger": "RANSOM",   "obligation": "extortion-reporting + regulator",
     "timeline": "24h class",     "prerequisite": "containment"},
]

TRIGGERS = tuple(d["trigger"] for d in DISCLOSURE)

# ── The reasoning engine ─────────────────────────────────────────────────────
# Signal regex → harvestable plane. Confirmed access implies data that SHOULD
# exist; reason names it, hunt proves it, crown registers it — counts only.

SIGNALS = [
    {"re": r"sql|database|\bdb\b|select count|table|schema",
     "plane": "SQL plane", "cls": "PII",
     "asset": "database tables + row counts",
     "probe": "SELECT table_name, table_rows FROM information_schema.tables",
     "proof": "table list + counts (read-only)"},
    {"re": r"s3|bucket|object store|minio|blob",
     "plane": "object storage", "cls": "BACKUP",
     "asset": "bucket key inventory",
     "probe": "bucket listing: keys + prefixes + sizes (read-only)",
     "proof": "key count + largest prefixes"},
    {"re": r"admin|tenant|saas|export|workspace",
     "plane": "SaaS admin", "cls": "SASS",
     "asset": "tenant export inventory + member counts",
     "probe": "export-config list + member count (read-only)",
     "proof": "export scope + member count"},
    {"re": r"repo|source|github|gitlab|commit",
     "plane": "source plane", "cls": "SRC",
     "asset": "repo inventory + secret-class counts",
     "probe": "repo list + secret scan (operator-owned code)",
     "proof": "repos + secret classes found"},
    {"re": r"ssh|shell|root|host|server|rce",
     "plane": "host filesystem", "cls": "CRED",
     "asset": "env vars + key files + cron entries",
     "probe": "listing: ~/.ssh, /etc/cron*, process env (read-only)",
     "proof": "counts + paths, never contents"},
    {"re": r"key|secret|token|firmware|device|kairo",
     "plane": "keyring/device", "cls": "CRED",
     "asset": "key/cert inventory",
     "probe": "keyring + cert store counts (read-only)",
     "proof": "key classes + counts"},
    {"re": r"http|url|web|api|endpoint|route",
     "plane": "harvest surface", "cls": "BACKUP",
     "asset": "exposed dumps/exports/env/config paths",
     "probe": "GET-only harvest-surface probe (see: hunt --live)",
     "proof": "200s with body sizes — nothing downloaded"},
]

# The harvest surface — data-plane paths GET-probed by `hunt --live`.
HARVEST_SURFACE = [
    "backup.zip", "backup.tar.gz", "backup.sql", "backups/", "dump.sql", "db.sql",
    "database.sql", "db.sqlite", "database.sqlite", "dump/", ".env", ".env.bak",
    ".git/config", ".git/HEAD", "config.php.bak", "wp-config.php.bak",
    "web.config.bak", "composer.json", "admin/backups/", "admin/export",
    "api/export", "api/exports", "api/admin/export", "export", "exports/",
    "debug/vars", "phpinfo.php", "server-status", ".DS_Store",
    "backups/backup.zip", "backup/backend.zip", "db/backup.sql", "site.zip",
    "website-backup.zip", "old/", "staging/", "test/", "dev/", "config.json",
    "config.yml", "config.yaml", "settings.py", "app.config", ".env.local",
    ".env.production", "environment.properties", "application.properties",
    "admin/db/", "admin/backup", "manager/backups", "api/admin/backup",
    "api/export/users", "api/export/all", "export/users.csv", "users.csv",
    "customers.csv", "orders.csv", "admin/users", "actuator/heapdump",
    "actuator/env", "debug/pprof", "server-info", ".gitlab-ci.yml",
    "Jenkinsfile", ".circleci/config.yml", "composer.lock", "yarn.lock",
]

# ── The feed engine ──────────────────────────────────────────────────────────
# Harvest discovery → family attack material. Documented classes only: every
# fed vector is a (flaw, seam) from 3AM's canon aimed at the seam that let the
# harvest happen. KAIRO ingests the family states on its next run.

FLAW_NAMES = {1: "validation-order", 2: "trust-in-client-params", 3: "type-coercion",
              4: "rate-limiter-scope", 5: "state-machine-gaps", 6: "identifier-trust",
              7: "cache/edge-separation", 8: "session/cookie-confusion",
              9: "header/parser-differential", 10: "entropy/forge",
              11: "observable-oracle", 12: "llm-data-plane", 13: "cloud-misconfig",
              14: "network-protocol", 15: "database-exposure", 16: "mobile-device",
              17: "firmware-hardware", 18: "wireless-rf", 19: "collab-webhook",
              20: "operational-planes"}
SEAM_NAMES = {"A": "CDN<->origin", "B": "client<->server-validation",
              "C": "auth<->backend-binding", "D": "limiter<->coercion",
              "E": "ws-handshake<->frame-auth", "F": "oauth<->app",
              "G": "edgefn<->db", "H": "multi-host-family", "I": "i18n/asset-plane",
              "J": "llm-layer", "K": "cloud-policy", "L": "device-firmware",
              "M": "protocol-handshake", "N": "collab-app", "O": "monitoring-plane"}

FED_RULES = [
    {"re": r"backup|dump|\.sql|\.sqlite|archive", "flaw": 13, "seam": "K",
     "probe": "GET the exposed dump/backup path on the own estate",
     "confirmed_when": "200 + archive/sql body — bulk artifact reachable"},
    {"re": r"\.env|\.git|config", "flaw": 15, "seam": "G",
     "probe": "GET the exposed env/config path on the own estate",
     "confirmed_when": "config body readable — data plane named"},
    {"re": r"export|admin", "flaw": 6, "seam": "C",
     "probe": "export enumeration on the own tenant",
     "confirmed_when": "export scope exceeds entitlement — boundary seam"},
    {"re": r"database|table|schema", "flaw": 15, "seam": "G",
     "probe": "schema enumeration via harvested access (own estate)",
     "confirmed_when": "table list + counts readable"},
]


def state_path(c):
    return Path.home() / ".redteam" / "campaigns" / c / "harvest-state.json"


def load(c):
    p = state_path(c)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def save(c, st):
    p = state_path(c)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, indent=2) + "\n")


def base(c):
    st = load(c)
    if st is None:
        st = {"campaign": c, "ingested": [], "crown": [], "excluded": [],
              "disclosures": [], "hypotheses": [], "hunted": [], "fed": [],
              "created": datetime.now(timezone.utc).isoformat()}
        save(c, st)
    for k in ("excluded", "hypotheses", "hunted", "fed"):
        st.setdefault(k, [])
    return st


def now():
    return datetime.now(timezone.utc).isoformat()


def finding_ids(st):
    return {i.get("finding") for i in st.get("ingested", [])}


def _campaign_signals(c):
    """All textual evidence available to the reasoner: ingested findings+proofs,
    undercroft ledgers, kairo device notes — the campaign's confirmed access."""
    sig = []
    st = load(c) or {}
    for i in st.get("ingested", []):
        sig.append(("finding", i.get("finding", ""), i.get("proof", "")))
    uc = Path.home() / ".redteam" / "campaigns" / c / "undercroft-state.json"
    try:
        u = json.loads(uc.read_text())
        for s in u.get("surface", []):
            if s.get("status") == "CONFIRMED":
                sig.append(("undercroft-surface", s.get("endpoint", ""),
                            s.get("proof", "")))
        for l in u.get("logic", []):
            if l.get("status") == "CONFIRMED":
                sig.append(("undercroft-logic", l.get("seam", ""),
                            l.get("proof", "")))
        for co in u.get("code", []):
            sig.append(("undercroft-code", co.get("asset", ""), co.get("note", "")))
    except Exception:
        pass
    hw = Path.home() / ".redteam" / "campaigns" / c / "hardware-state.json"
    try:
        h = json.loads(hw.read_text())
        for d in h.get("devices", []):
            for n in d.get("notes", []):
                sig.append(("kairo-device", d.get("name", ""),
                            n.get("finding", "")))
    except Exception:
        pass
    return sig


def cmd_ingest(args):
    st = base(args.target)
    ing = st.setdefault("ingested", [])
    if any(i.get("finding") == args.finding for i in ing):
        print(f"· finding '{args.finding}' already ingested — skipping")
        return 0
    ing.append({"finding": args.finding, "proof": args.proof, "at": now()})
    save(args.target, st)
    print(f"▸ ingested: {args.finding} (proof: {args.proof[:70]})")
    return 0


def cmd_reason(args):
    st = base(args.target)
    if not st.get("ingested"):
        print("✗ nothing ingested — reason works from CONFIRMED access; run"
              " `ingest` first (a hypothesis with no source is a fabrication)",
              file=sys.stderr)
        return 2
    sig = _campaign_signals(args.target)
    seen, hyps = set(), []
    for rule in SIGNALS:
        for k, a, b in sig:
            if not re.search(rule["re"], f"{a} {b}".lower()):
                continue
            key = (rule["plane"], a or b)
            if key in seen:
                continue
            seen.add(key)
            hyps.append({"plane": rule["plane"], "asset": rule["asset"],
                         "class": rule["cls"], "probe": rule["probe"],
                         "proof": rule["proof"], "source": a or b,
                         "status": "OPEN", "at": now()})
    # crown drift: registered assets must be re-verified (findings decay)
    for cr in st.get("crown", []):
        hyps.append({"plane": "drift", "asset": f"re-verify: {cr['asset']}",
                     "class": cr["class"],
                     "probe": "re-run the read-only reach proof (counts, never contents)",
                     "proof": "count matches registered scope", "source": cr["source"],
                     "status": "OPEN", "at": now()})
    rank = {c: i for i, c in enumerate(CLASSES)}
    hyps.sort(key=lambda h: rank.get(h["class"], 99))
    for i, h in enumerate(hyps):
        h["id"] = f"H-{i + 1:03d}"
    st["hypotheses"] = hyps
    save(args.target, st)
    if args.json:
        print(json.dumps(hyps, indent=2))
        return 0
    print(f"═══ SHUKAKU reason — what SHOULD be harvestable ({len(hyps)} hypotheses) ═══")
    for h in hyps:
        print(f"  {h['id']} [{h['class']:6s}] {h['plane']:16s} {h['asset']}")
        print(f"         source: {h['source'][:64]}")
        print(f"         probe:  {h['probe'][:92]}")
    print("")
    print(f"  next: hunt --target {args.target}   (read-only proofs — static or --live)")
    return 0


def _scope_gate(value):
    """The scope authority (~/.redteam/scope.json): True=in scope, False=out,
    None=no authority (ungated legacy mode)."""
    sp = Path.home() / ".redteam" / "scope.json"
    if not sp.exists():
        return None
    try:
        scope = json.loads(sp.read_text())
    except Exception:
        return None
    from urllib.parse import urlparse
    v = value.strip().lower()
    host = urlparse(v).hostname or v if "://" in v else v
    for o in scope.get("out_of_scope", []):
        if host == o.lower() or host.endswith("." + o.lower()):
            return False
    for i in scope.get("in_scope", []):
        i = i.lower()
        ih = urlparse(i).hostname or i if "://" in i else i
        if host == ih or host.endswith("." + ih):
            return True
    return False


def cmd_hunt(args):
    st = base(args.target)
    if args.live:
        if not args.live.startswith(("http://", "https://")):
            print("✗ --live wants a base URL (http/https)", file=sys.stderr)
            return 2
        if not args.dry_run:
            gate = _scope_gate(args.live)
            if gate is False:
                print("✗ SCOPE CLOSED — live harvest refuses out-of-scope targets"
                      " (spydermonkey scope check --value <url>)", file=sys.stderr)
                return 1
        base_url = args.live.rstrip("/")
        cands = [f"{base_url}/{w}" for w in HARVEST_SURFACE][: (args.max or 999)]
        if args.dry_run:
            print(f"▸ dry-run — {len(cands)} GET-only harvest-surface candidates:")
            for u in cands:
                print(f"    {u}")
            return 0
        hdrs = {"User-Agent": "SHUKAKU-harvest/read-only"}
        if args.cookie:
            hdrs["Cookie"] = args.cookie
        print(f"▸ hunt --live: {len(cands)} GET-only probes (0.2s pacing, burst"
              " pauses) — catalog-only, nothing is downloaded")
        hits, burst = [], 0
        for u in cands:
            try:
                req = urllib.request.Request(u, headers=hdrs, method="GET")
                with urllib.request.urlopen(req, timeout=6) as r:
                    code_, blen = r.status, len(r.read(4096))
            except urllib.error.HTTPError as e:
                code_, blen = e.code, 0
            except Exception:
                code_, blen = 0, 0
            burst += 1
            time.sleep(1.0 if burst % 25 == 0 else 0.2)
            if code_ == 200:
                hits.append({"url": u, "code": code_, "bytes": blen,
                             "status": "CONFIRMED", "at": now()})
                print(f"    HARVESTABLE 200  {u}  ({blen}B)")
        known = {h["url"] for h in st.get("hunted", [])}
        st.setdefault("hunted", []).extend(
            h for h in hits if h["url"] not in known)
        save(args.target, st)
        print(f"▸ hunt done: {len(hits)} harvestable path(s) confirmed"
              f" (registered: {len(st['hunted'])} total)")
        print("  next: crown --asset <path> --source <finding> … then feed")
        return 0
    if not st.get("hypotheses"):
        print("✗ no hypotheses — run `reason` first (hunt works the reasoned planes)",
              file=sys.stderr)
        return 2
    open_h = [h for h in st["hypotheses"] if h["status"] == "OPEN"]
    print(f"═══ SHUKAKU hunt — {len(open_h)} open hypotheses → exact read-only proofs ═══")
    for h in open_h:
        print(f"  {h['id']} [{h['class']:6s}] {h['asset']}")
        print(f"         run:  {h['probe']}")
        print(f"         proof when done: {h['proof']}")
    print("")
    print("  (static mode never executes anything — the proofs are yours to run;")
    print("   --live URL adds GET-only harvest-surface probes, catalog-only)")
    for h in open_h:
        h["status"] = "HUNTED"
    save(args.target, st)
    return 0


def cmd_crown(args):
    st = base(args.target)
    if args.cls not in CLASSES:
        print(f"✗ class must be one of {CLASSES}", file=sys.stderr)
        return 2
    if not args.scope:
        print("✗ scope required — counts, never contents", file=sys.stderr)
        return 2
    # Evidence-chain rule 2: SOURCE must be a real ingested finding ID.
    if not args.source:
        print("✗ --source required: a harvest entry with no source is a fabrication"
              " — ingest the finding first", file=sys.stderr)
        return 2
    if args.source not in finding_ids(st):
        known = ", ".join(sorted(finding_ids(st))) or "(none ingested)"
        print(f"✗ source '{args.source}' is not an ingested finding — fabrications"
              f" refuse. ingested: {known}", file=sys.stderr)
        return 2
    # Proof of the source finding must exist (evidence-chain rule 3).
    proof = next((i["proof"] for i in st["ingested"] if i["finding"] == args.source), "")
    # Valuation: value must carry an ESTIMATE label with a basis (rule: no
    # invented precision).
    if args.value:
        if "estimate" not in args.value.lower():
            print("✗ value must be labeled $ESTIMATE — a single-number price without"
                  " basis is a violation (see: shukaku ladder)", file=sys.stderr)
            return 2
        value = args.value
        basis = args.basis or "market-ladder"
    else:
        row = LADDER[args.cls][0]
        value = f"{row['range']} ({row['unit']})"
        basis = args.basis or f"market-ladder: {row['basis']}"
    crown = st.setdefault("crown", [])
    entry = {"id": f"crown-{len(crown) + 1:03d}", "asset": args.asset,
             "class": args.cls, "scope": args.scope, "value": value,
             "basis": basis, "source": args.source, "proof": proof, "at": now()}
    crown.append(entry)
    # close the hypotheses this crown answers
    for h in st.get("hypotheses", []):
        if h["status"] == "OPEN" and (h["asset"] in args.asset
                                      or args.asset in h["asset"]):
            h["status"] = "HARVESTED"
    save(args.target, st)
    print(f"▸ crown: {entry['id']} {args.asset} [{args.cls}] {args.scope} — {value}")
    return 0


def cmd_exclude(args):
    st = base(args.target)
    st.setdefault("excluded", []).append({"finding": args.finding,
                                          "reason": args.reason, "at": now()})
    save(args.target, st)
    print(f"▸ excluded: {args.finding} — {args.reason[:80]}")
    return 0


def cmd_disclose(args):
    st = base(args.target)
    if args.add:
        obligation = args.add
    elif args.trigger:
        row = next((d for d in DISCLOSURE if d["trigger"] == args.trigger), None)
        if row is None:
            print(f"✗ trigger must be one of {TRIGGERS}", file=sys.stderr)
            return 2
        obligation = f"{row['obligation']} · {row['timeline']} · {row['prerequisite']}"
        if args.note:
            obligation += f" — {args.note}"
    else:
        print("✗ disclose needs --trigger <T> or --add \"…\"", file=sys.stderr)
        return 2
    st.setdefault("disclosures", []).append({"obligation": obligation, "at": now()})
    save(args.target, st)
    print(f"▸ disclosure: {obligation[:90]}")
    return 0


def cmd_feed(args):
    """Harvest → family: 3AM vectors, undercroft CONFIRMED surface, holyshit
    recipe cards. KAIRO ingests the family states on its next run — the loop
    closes: the next assault starts smarter."""
    st = base(args.target)
    if not st.get("crown") and not st.get("hunted"):
        print("✗ nothing harvested yet — crown or hunt first; a fed vector with no"
              " harvest behind it is a fabrication", file=sys.stderr)
        return 2
    fed = st.setdefault("fed", [])
    fed_keys = {(f.get("kind"), f.get("what"), f.get("to")) for f in fed}
    out3am, outuc, outrecipes = [], [], []

    def feed3am(kind, what, flaw, seam, probe, confirmed_when, src):
        if (kind, what, "3AM") in fed_keys:
            return
        out3am.append({"flaw": flaw, "flaw_name": FLAW_NAMES[flaw], "seam": seam,
                       "seam_name": SEAM_NAMES[seam], "probe": probe,
                       "confirmed_when": confirmed_when,
                       "source": f"SHUKAKU {kind}: {src}", "learned_at": now()})
        fed.append({"kind": kind, "what": what, "to": "3AM", "at": now()})
        fed_keys.add((kind, what, "3AM"))

    def feeduc(kind, what, endpoint, adkind, proof):
        if (kind, what, "undercroft") in fed_keys:
            return
        outuc.append({"endpoint": endpoint, "kind": adkind, "status": "CONFIRMED",
                      "proof": proof, "at": now()})
        fed.append({"kind": kind, "what": what, "to": "undercroft", "at": now()})
        fed_keys.add((kind, what, "undercroft"))

    def feedrecipe(kind, what, asset, cls, proof):
        if (kind, what, "holyshit") in fed_keys:
            return
        outrecipes.append(
            f"### SHUKAKU-HARVEST {asset} — {cls} (source: {kind})\n"
            f"- what: {what}\n- proof (read-only): {proof}\n"
            f"- use: sweep the seam that exposed it; crown its data plane\n")
        fed.append({"kind": kind, "what": what, "to": "holyshit", "at": now()})
        fed_keys.add((kind, what, "holyshit"))

    # 1. crown entries → 3AM vectors (+ recipes for bulk/source assets)
    for cr in st.get("crown", []):
        src = f"{cr['asset']} [{cr['class']}]"
        if cr["class"] == "BACKUP":
            r = FED_RULES[0]
            feed3am("crown", cr["id"], r["flaw"], r["seam"], r["probe"],
                    r["confirmed_when"], src)
            feedrecipe("crown", cr["id"], cr["asset"], cr["class"], cr["proof"])
        elif cr["class"] in ("PII", "FIN"):
            r = FED_RULES[3]
            feed3am("crown", cr["id"], r["flaw"], r["seam"], r["probe"],
                    r["confirmed_when"], src)
        elif cr["class"] == "SASS":
            r = FED_RULES[2]
            feed3am("crown", cr["id"], r["flaw"], r["seam"], r["probe"],
                    r["confirmed_when"], src)
            feeduc("crown", cr["id"], cr["asset"], "admin",
                   f"SHUKAKU crown {cr['id']}: {cr['proof'][:60]}")
        elif cr["class"] == "SRC":
            feed3am("crown", cr["id"], 2, "B",
                    "client-side secrets in shipped bundle/source (own estate)",
                    "secret-class strings found — documented scanner classes",
                    src)
            feedrecipe("crown", cr["id"], cr["asset"], cr["class"], cr["proof"])
        elif cr["class"] == "CRED":
            feed3am("crown", cr["id"], 10, "C",
                    "credential-reuse check on the own estate (harvested creds)",
                    "second system accepts — documented reuse classes",
                    src)

    # 2. hunted CONFIRMED paths → undercroft surface + 3AM vectors + recipes
    for h in st.get("hunted", []):
        if h.get("status") != "CONFIRMED":
            continue
        path = h["url"].split("//", 1)[-1].split("/", 1)[-1] or "/"
        rule = next((r for r in FED_RULES if re.search(r["re"], path.lower())),
                    FED_RULES[2])
        feed3am("hunt", h["url"], rule["flaw"], rule["seam"],
                f"GET {h['url']} (own estate, read-only)",
                f"200 confirmed by SHUKAKU hunt ({h['bytes']}B) —"
                f" {rule['confirmed_when']}", path)
        feeduc("hunt", h["url"], "/" + path,
               "admin" if "admin" in path.lower() else "hidden",
               f"SHUKAKU hunt: HTTP {h['code']} ({h['bytes']}B)")
        feedrecipe("hunt", h["url"], path, "HARVEST-SURFACE",
                   f"GET → 200 ({h['bytes']}B)")

    # write the drops
    wrote = []
    if out3am:
        learned = Path.home() / ".redteam" / "learned-vectors.jsonl"
        learned.parent.mkdir(parents=True, exist_ok=True)
        with learned.open("a") as f:
            for row in out3am:
                f.write(json.dumps(row) + "\n")
        wrote.append(f"3AM: {len(out3am)} vector row(s) → {learned}")
    if outuc:
        uc = Path.home() / ".redteam" / "campaigns" / args.target / "undercroft-state.json"
        try:
            u = json.loads(uc.read_text()) if uc.exists() else {"target": args.target}
        except Exception:
            u = {"target": args.target}
        u.setdefault("surface", []).extend(outuc)
        uc.parent.mkdir(parents=True, exist_ok=True)
        uc.write_text(json.dumps(u, indent=2) + "\n")
        wrote.append(f"undercroft: {len(outuc)} CONFIRMED surface entr(y/ies) → {uc}")
    if outrecipes:
        recipes = Path.home() / ".redteam" / "synthesized-recipes.md"
        recipes.parent.mkdir(parents=True, exist_ok=True)
        with recipes.open("a") as f:
            f.write("\n".join(outrecipes) + "\n")
        wrote.append(f"holyshit: {len(outrecipes)} recipe card(s) → {recipes}")
    save(args.target, st)
    print("▸ SHUKAKU feeds the family — the next assault starts smarter:")
    for w in wrote:
        print(f"    {w}")
    if not wrote:
        print("    (everything already fed — never double-shipped)")
    print(f"  next: 3AM promote --apply --verified · kairo ingest --target {args.target}")
    return 0


def cmd_ladder(args):
    if args.cls:
        if args.cls not in LADDER:
            print(f"✗ class must be one of {CLASSES}", file=sys.stderr)
            return 2
        rows = [(args.cls, r) for r in LADDER[args.cls]]
    else:
        rows = [(cls, r) for cls, r in LADDER.items() for r in r]
    print("═══ SHUKAKU valuation ladder — ESTIMATE ranges, never invented precision ═══")
    for cls, r in rows:
        print(f"  {cls:6s} {r['market']:28s} {r['unit']:16s} {r['range']}")
        print(f"         basis: {r['basis']}")
    print("")
    print("═══ disclosure map — what a breached org would owe ═══")
    for d in DISCLOSURE:
        print(f"  {d['trigger']:9s} {d['obligation']:38s} {d['timeline']:16s}"
              f" prereq: {d['prerequisite']}")
    print("")
    print("  catalog, never collect · register keeps counts, never corpora")
    return 0


def _maps(d, c):
    """Does a disclosure obligation row cover a crown entry's class?"""
    o = d["obligation"].lower()
    if c["class"] == "PII":
        return "state ag" in o or "gdpr" in o
    if c["class"] == "FIN":
        return "card" in o
    if c["class"] == "BACKUP":
        return "extortion" in o
    return False  # CRED/SRC/SASS: org-policy classes are added manually


def cmd_report(args):
    st = base(args.target)
    out = args.output or f"{args.target}-shukaku-report.md"
    crown, ing = st.get("crown", []), st.get("ingested", [])
    excl, disc = st.get("excluded", []), st.get("disclosures", [])
    hyps, hunted, fed = st.get("hypotheses", []), st.get("hunted", []), st.get("fed", [])
    ids = finding_ids(st)
    L = [f"# SHUKAKU Harvest Report — {args.target}", "",
         "_the business-impact verdict layer (P5) · catalog-only · nothing moved_",
         "", "## Ingested findings"]
    L += [f"- {i['finding']} (proof: {i['proof']})" for i in ing] or ["- none"]
    if hyps:
        L += ["", "## Harvest hypotheses (what SHOULD be harvestable)"]
        L += [f"- **{h['id']}** [{h['class']}] {h['plane']} — {h['asset']}"
              f" · {h['status']} · source: {h['source']}" for h in hyps]
    if hunted:
        L += ["", "## Hunt results (read-only, catalog-only)"]
        L += [f"- HARVESTABLE {h['code']} {h['url']} ({h['bytes']}B)"
              for h in hunted]
    L += ["", "## Crown register (the crown-entry standard)"]
    for c in crown:
        L += ["```",
              f"SOURCE: {c.get('source', '—'):34s} PROOF: {c.get('proof', '—')}",
              f"ASSET:  {c['asset']:34s} SCOPE: {c['scope']}",
              f"CLASS:  {c['class']:34s} VALUE: {c['value']} (basis: {c.get('basis', '—')})",
              f"DISCLOSE: {next((d['obligation'] for d in disc if _maps(d, c)), 'unmapped — map before closeout')}",
              "```", ""]
    if not crown:
        L.append("- (empty — every finding must chain to a crown entry or be excluded)")
    L += ["", "## Valuation summary"]
    for cls in CLASSES:
        rows = [c for c in crown if c["class"] == cls]
        if rows:
            L.append(f"- **{cls}**: {len(rows)} asset(s) — "
                     + "; ".join(f"{c['asset']} {c['value']}" for c in rows))
    if not crown:
        L.append("- (nothing registered)")
    L += ["", "## Disclosure map"]
    L += [f"- {d['obligation']}" for d in disc] or ["- (none mapped)"]
    prereqs = []
    for d in disc:
        parts = [p.strip() for p in d["obligation"].split("·")]
        if len(parts) >= 3:
            prereqs.append(parts[2].split(" — ")[0].strip())
    if prereqs:
        L += ["", "## Remediation prerequisites (before closeout)"]
        L += [f"- {p}" for p in dict.fromkeys(prereqs)]
    if fed:
        L += ["", "## Fed back to the family (the loop)"]
        L += [f"- {f['to']}: {f['what']}" for f in fed]
    if excl:
        L += ["", "## Excluded findings (with reasons — never padded)"]
        L += [f"- {e['finding']} — {e['reason']}" for e in excl]
    warn = []
    unharvested = [f for f in sorted(ids)
                   if not any(c.get("source") == f for c in crown)
                   and not any(e.get("finding") == f for e in excl)]
    if unharvested:
        warn.append(f"ingested without crown entry or exclusion: {', '.join(unharvested)}")
    unmapped = [c["id"] for c in crown if not any(_maps(d, c) for d in disc)]
    if unmapped:
        warn.append(f"crown entries with no disclosure mapping: {', '.join(unmapped)}")
    open_h = [h["id"] for h in hyps if h["status"] == "OPEN"]
    if open_h:
        warn.append(f"hypotheses still open (hunt them): {', '.join(open_h)}")
    if warn:
        L += ["", "## Integrity warnings"]
        L += [f"- ⚠ {w}" for w in warn]
    Path(out).write_text("\n".join(L) + "\n")
    print(f"▸ report written: {out} ({len(crown)} crown · {len(hunted)} hunted ·"
          f" {len(fed)} fed · {len(excl)} excluded · {len(disc)} disclosures)")
    return 0


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    if subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                      capture_output=True).returncode != 0:
        bad.append("compile")
    help_out = subprocess.run([sys.executable, str(self), "--help"],
                              capture_output=True, text=True).stdout
    for want in ("ingest", "reason", "hunt", "crown", "exclude", "disclose",
                 "feed", "ladder", "report", "verify"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    root = self.parent.parent
    tmpl = root / "templates" / "harvest-state.json"
    try:
        t = json.loads(tmpl.read_text())
        for k in ("ingested", "crown", "excluded", "disclosures", "hypotheses",
                  "hunted", "fed"):
            if k not in t:
                bad.append(f"template key {k}")
    except Exception:
        bad.append("template json")
    pb = root / "references" / "harvest-playbook.md"
    if not pb.exists():
        bad.append("playbook file")
    if set(LADDER) != set(CLASSES):
        bad.append("ladder coverage")
    if len(DISCLOSURE) != 6:
        bad.append("disclosure map rows")
    if set(FLAW_NAMES) != set(range(1, 21)):
        bad.append("3AM flaw table")
    if len(SEAM_NAMES) != 15:
        bad.append("3AM seam table")
    if bad:
        print(f"✗ SHUKAKU verify FAILED: {bad}")
        return 1
    print("✓ SHUKAKU verify: compile · subcommands · template · ladder · disclosure"
          " map · 3AM schema · reason/hunt/feed — ALL PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description="SHUKAKU — Harvest Mandate CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="ingest a confirmed finding")
    i.add_argument("--target", required=True)
    i.add_argument("--finding", required=True)
    i.add_argument("--proof", required=True, help="reproducible read-only proof ref")
    rea = sub.add_parser("reason", help="infer what SHOULD be harvestable")
    rea.add_argument("--target", required=True)
    rea.add_argument("--json", action="store_true")
    hu = sub.add_parser("hunt", help="work the hypotheses (read-only)")
    hu.add_argument("--target", required=True)
    hu.add_argument("--live", help="GET-only harvest-surface probe against a base URL")
    hu.add_argument("--cookie", help="k=v cookie for live probes")
    hu.add_argument("--max", type=int, help="cap live candidates")
    hu.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("crown", help="register a crown entry (evidence-chain enforced)")
    c.add_argument("--target", required=True)
    c.add_argument("--asset", required=True)
    c.add_argument("--class", dest="cls", required=True, choices=CLASSES)
    c.add_argument("--scope", required=True, help="counts, never contents")
    c.add_argument("--source", required=True, help="ingested finding ID")
    c.add_argument("--value", help="$ESTIMATE range (defaults from the ladder)")
    c.add_argument("--basis", help="market-ladder | benchmark | disclosed demand")
    e = sub.add_parser("exclude", help="exclude a finding with a reason")
    e.add_argument("--target", required=True)
    e.add_argument("--finding", required=True)
    e.add_argument("--reason", required=True)
    d = sub.add_parser("disclose", help="map a disclosure obligation")
    d.add_argument("--target", required=True)
    d.add_argument("--trigger", choices=TRIGGERS, help="pull a playbook trigger row")
    d.add_argument("--add", help="freeform \"<obligation> · <timeline> · <prerequisite>\"")
    d.add_argument("--note")
    f = sub.add_parser("feed", help="harvest → family (3AM · undercroft · holyshit)")
    f.add_argument("--target", required=True)
    ld = sub.add_parser("ladder", help="the valuation ladder + disclosure map")
    ld.add_argument("--class", dest="cls", choices=CLASSES)
    r = sub.add_parser("report", help="harvest deliverable (crown-entry standard)")
    r.add_argument("--target", required=True)
    r.add_argument("--output")
    v = sub.add_parser("verify", help="self-check")
    a = ap.parse_args()
    dispatch = {"ingest": cmd_ingest, "reason": cmd_reason, "hunt": cmd_hunt,
                "crown": cmd_crown, "exclude": cmd_exclude,
                "disclose": cmd_disclose, "feed": cmd_feed, "ladder": cmd_ladder,
                "report": cmd_report, "verify": cmd_verify}
    return dispatch[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
