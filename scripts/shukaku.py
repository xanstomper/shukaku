#!/usr/bin/env python3
"""
SHUKAKU — Harvest Mandate CLI. Catalog · price · disclose (validation-only).
stdlib-only. State: ~/.redteam/campaigns/<campaign>/harvest-state.json.

Commands:
  ingest    --target <c> --finding "<id>" --proof "<read-only proof ref>"
  crown     --target <c> --asset "<table|bucket|export>" --class PII|FIN|CRED|BACKUP|SRC|SASS
            --scope "<counts, not contents>" --source "<ingested finding ID>"
            [--value "$ESTIMATE ..."] [--basis "..."]
  exclude   --target <c> --finding "<id>" --reason "no data reach | out of scope | wall"
  disclose  --target <c> --trigger PII-US|PII-EU|FIN|HEALTH|CONTRACT|RANSOM [--note "..."]
            [--add "<obligation> · <timeline> · <prerequisite>"]
  ladder    [--class C]      the valuation ladder + disclosure map (playbook canon)
  report    --target <c> [--output F]   the harvest deliverable (crown-entry standard)
  verify    self-check

Exit codes: 0 ok · 1 verify failure · 2 usage/state error.
"""
import argparse
import json
import subprocess
import sys
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
              "disclosures": [], "created": datetime.now(timezone.utc).isoformat()}
        save(c, st)
    st.setdefault("excluded", [])
    return st


def now():
    return datetime.now(timezone.utc).isoformat()


def finding_ids(st):
    return {i.get("finding") for i in st.get("ingested", [])}


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


def cmd_report(args):
    st = base(args.target)
    out = args.output or f"{args.target}-shukaku-report.md"
    crown, ing = st.get("crown", []), st.get("ingested", [])
    excl, disc = st.get("excluded", []), st.get("disclosures", [])
    ids = finding_ids(st)
    L = [f"# SHUKAKU Harvest Report — {args.target}", "",
         f"_the business-impact verdict layer (P5) · catalog-only · nothing moved_",
         "", "## Ingested findings"]
    L += [f"- {i['finding']} (proof: {i['proof']})" for i in ing] or ["- none"]
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
    # Valuation summary per class.
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
    if excl:
        L += ["", "## Excluded findings (with reasons — never padded)"]
        L += [f"- {e['finding']} — {e['reason']}" for e in excl]
    # Integrity warnings.
    warn = []
    unharvested = [f for f in sorted(ids)
                   if not any(c.get("source") == f for c in crown)
                   and not any(e.get("finding") == f for e in excl)]
    if unharvested:
        warn.append(f"ingested without crown entry or exclusion: {', '.join(unharvested)}")
    unmapped = [c["id"] for c in crown
                if not any(_maps(d, c) for d in disc)]
    if unmapped:
        warn.append(f"crown entries with no disclosure mapping: {', '.join(unmapped)}")
    if warn:
        L += ["", "## Integrity warnings"]
        L += [f"- ⚠ {w}" for w in warn]
    Path(out).write_text("\n".join(L) + "\n")
    print(f"▸ report written: {out} ({len(crown)} crown · {len(excl)} excluded ·"
          f" {len(disc)} disclosures)")
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


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    if subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                      capture_output=True).returncode != 0:
        bad.append("compile")
    help_out = subprocess.run([sys.executable, str(self), "--help"],
                              capture_output=True, text=True).stdout
    for want in ("ingest", "crown", "exclude", "disclose", "ladder", "report",
                 "verify"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    root = self.parent.parent
    tmpl = root / "templates" / "harvest-state.json"
    try:
        t = json.loads(tmpl.read_text())
        for k in ("ingested", "crown", "excluded", "disclosures"):
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
    if bad:
        print(f"✗ SHUKAKU verify FAILED: {bad}")
        return 1
    print("✓ SHUKAKU verify: compile · subcommands · template · ladder ·"
          " disclosure map — ALL PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description="SHUKAKU — Harvest Mandate CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="ingest a confirmed finding")
    i.add_argument("--target", required=True)
    i.add_argument("--finding", required=True)
    i.add_argument("--proof", required=True, help="reproducible read-only proof ref")
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
    ld = sub.add_parser("ladder", help="the valuation ladder + disclosure map")
    ld.add_argument("--class", dest="cls", choices=CLASSES)
    r = sub.add_parser("report", help="harvest deliverable (crown-entry standard)")
    r.add_argument("--target", required=True)
    r.add_argument("--output")
    v = sub.add_parser("verify", help="self-check")
    a = ap.parse_args()
    dispatch = {"ingest": cmd_ingest, "crown": cmd_crown, "exclude": cmd_exclude,
                "disclose": cmd_disclose, "ladder": cmd_ladder,
                "report": cmd_report, "verify": cmd_verify}
    return dispatch[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
