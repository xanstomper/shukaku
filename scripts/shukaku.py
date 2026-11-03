#!/usr/bin/env python3
"""
SHUKAKU — Harvest Mandate CLI. Catalog · price · disclose (validation-only).
stdlib-only. State: ~/.redteam/campaigns/<campaign>/harvest-state.json.

Commands:
  ingest    --target <c> --finding "<id>" --proof "<read-only proof ref>"
  crown     --target <c> --asset "<table|bucket|export>" --class PII|FIN|CRED|BACKUP|SRC|SASS
            --scope "<counts, not contents>" [--value "$ESTIMATE"] [--basis "..."]
  disclose  --target <c> --add "<obligation> · <timeline> · <prerequisite>"
  report    --target <c> [--output F]
  verify    self-check

Exit codes: 0 ok · 2 usage/state error.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CLASSES = ("PII", "FIN", "CRED", "BACKUP", "SRC", "SASS")


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
        st = {"campaign": c, "ingested": [], "crown": [], "disclosures": [],
              "created": datetime.now(timezone.utc).isoformat()}
        save(c, st)
    return st


def cmd_ingest(args):
    st = base(args.target)
    ing = st.setdefault("ingested", [])
    if any(i.get("finding") == args.finding for i in ing):
        print(f"· finding '{args.finding}' already ingested — skipping")
        return 0
    ing.append({"finding": args.finding, "proof": args.proof,
                "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    print(f"▸ ingested: {args.finding} (proof: {args.proof[:70]})")
    return 0


def cmd_crown(args):
    st = base(args.target)
    if args.cls not in CLASSES:
        print(f"✗ class must be one of {CLASSES}", file=sys.stderr)
        return 2
    crown = st.setdefault("crown", [])
    entry = {"asset": args.asset, "class": args.cls, "scope": args.scope,
             "value": args.value or "$ESTIMATE — TBD", "basis": args.basis or "",
             "source": args.source or "", "at": datetime.now(timezone.utc).isoformat()}
    crown.append(entry)
    save(args.target, st)
    print(f"▸ crown: {args.asset} [{args.cls}] {args.scope} {entry['value']}")
    return 0


def cmd_disclose(args):
    st = base(args.target)
    st.setdefault("disclosures", []).append({"obligation": args.add,
                                             "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    print(f"▸ disclosure: {args.add[:90]}")
    return 0


def cmd_report(args):
    st = base(args.target)
    out = args.output or f"{args.target}-shukaku-report.md"
    L = [f"# SHUKAKU Harvest Report — {args.target}", "",
         "## Ingested findings"]
    for i in st.get("ingested", []):
        L.append(f"- {i['finding']} (proof: {i['proof']})")
    if not st.get("ingested"):
        L.append("- none")
    L += ["", "## Crown register"]
    for c in st.get("crown", []):
        L.append(f"- **{c['asset']}** [{c['class']}] {c['scope']} — {c['value']}"
                 + (f" (basis: {c['basis']})" if c.get("basis") else "")
                 + (f" ← source: {c['source']}" if c.get("source") else ""))
    if not st.get("crown"):
        L.append("- (empty — every finding must chain to a crown entry)")
    L += ["", "## Disclosure map"]
    for d in st.get("disclosures", []):
        L.append(f"- {d['obligation']}")
    if not st.get("disclosures"):
        L.append("- (none mapped)")
    Path(out).write_text("\n".join(L) + "\n")
    print(f"▸ report written: {out}")
    return 0


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    if subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                      capture_output=True).returncode != 0:
        bad.append("compile")
    help_out = subprocess.run([sys.executable, str(self), "--help"],
                              capture_output=True, text=True).stdout
    for want in ("ingest", "crown", "disclose", "report", "verify"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    tmpl = Path(__file__).resolve().parent.parent / "templates" / "harvest-state.json"
    if tmpl.exists():
        try:
            json.loads(tmpl.read_text())
        except Exception:
            bad.append("template json")
    if bad:
        print(f"✗ SHUKAKU verify FAILED: {bad}")
        return 1
    print("✓ SHUKAKU verify: compile · subcommands · template — ALL PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description="SHUKAKU — Harvest Mandate CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="ingest a confirmed finding")
    i.add_argument("--target", required=True)
    i.add_argument("--finding", required=True)
    i.add_argument("--proof", required=True)
    c = sub.add_parser("crown", help="register a crown entry")
    c.add_argument("--target", required=True)
    c.add_argument("--asset", required=True)
    c.add_argument("--class", dest="cls", required=True, choices=CLASSES)
    c.add_argument("--scope", required=True)
    c.add_argument("--value")
    c.add_argument("--basis")
    c.add_argument("--source")
    d = sub.add_parser("disclose", help="map a disclosure obligation")
    d.add_argument("--target", required=True)
    d.add_argument("--add", required=True)
    r = sub.add_parser("report", help="harvest deliverable")
    r.add_argument("--target", required=True)
    r.add_argument("--output")
    v = sub.add_parser("verify", help="self-check")
    v.add_argument("--target")
    a = ap.parse_args()
    if a.cmd == "ingest":
        return cmd_ingest(a)
    if a.cmd == "crown":
        return cmd_crown(a)
    if a.cmd == "disclose":
        return cmd_disclose(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "verify":
        return cmd_verify(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())