---
name: shukaku
description: "Trigger `shukaku`. The Harvest Mandate — post-compromise data validation, valuation, and disclosure. What an attacker could take, priced and packaged."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, offensive-security, data-validation, breach-impact, disclosure, extortion-economy]
    related_skills: [holyshit-mode, 3am-shinjitsu, kairo]
---

# SHUKAKU (収穫) — The Harvest Mandate

The third role in the family chain. HolyShit **searches**, 3AM **attacks** —
SHUKAKU **harvests**: it answers the only question the family's verdicts exist for —

> **What did the attacker actually GAIN — in tables, rows, records, keys, and
> dollars — and who must be told?**

The cartel economy runs on data. SHUKAKU is the role that catalogs what a confirmed
compromise makes reachable (**without moving a single row**), prices it the way the
extortion market does, and builds the breach-disclosure package the operator's
organization would owe. It turns 3AM's compromises from technical findings into
business verdicts.

## The Family Tree (roles)

```
   THE HOLYSHIT FAMILY — one chain, four roles, one gate
   HolyShit!     3AM Shinjitsu       SHUKAKU             KAIRO
   (SEARCHER)    (ATTACKER)          (HARVESTER)         (the metal)
   finds what's  gets in, takes      catalogs · prices ·  hardware/firmware
   there ·       over, certifies     discloses what an    planes when devices
   65+ cases     chains (T1–T7)      attacker could take  enter the chain
```

- `holyshit-mode` — the searcher: recipes + discovery canon, normative by reference.
- `3am-shinjitsu` — the attacker: sweep, synthesis, takeover layers. SHUKAKU consumes
  its CONFIRMED findings and certified chains.
- `kairo` — the metal: hardware compromise findings (device data, keys, firmware
  secrets) enter the harvest register too.

## When to Use

Trigger `shukaku` when a compromise EXISTS — a CONFIRMED finding or certified chain
from 3AM/holyShit/KAIRO on a declared operator estate — and the engagement must answer
the harvest question: what data is reachable, what is it worth, and what must be
disclosed. SHUKAKU is the P4→P5 completing role: it runs alongside control proofs and
produces the closeout's impact layer.

## Activation

Run the trigger sequence ONCE, then collect P0 via the agent's question feature:

```text
▸ SHUKAKU — HARVEST MANDATE ARMED
  ═══════════════════════════════════
  [ OK ] crown register open
  [ OK ] valuation ladder loaded
  [ OK ] disclosure map ready
  ⚡ SHUKAKU ARMED · STATUS: READY
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: campaigns · authorization
```

**P0 (clarify, zero documents):** which campaigns/findings feed the harvest ·
objective · authorization. Recorded declaration = the entire gate (family canon).

## The Harvest Contract — validation-only, no exceptions

- **Catalog, never collect.** Reachable data is PROVEN read-only: schema counts,
  `SELECT count(*)`, bucket listings, export inventory. Sample ≤3 rows, redacted at
  capture. **Nothing is ever moved, copied, or exfiltrated** — the register is the
  deliverable, not the data.
- **Price like the market does.** Valuation tiers follow the observed extortion
  economy: customer PII (per-record street prices by jurisdiction), financial
  records, credentials, backups, source code, SaaS exports. Prices are labeled
  ESTIMATE ranges, never invented precision.
- **Disclose like the law does.** The disclosure map names what a breached org would
  owe: regulator obligations, notification timelines, affected-scope definition,
  remediation prerequisites. This is the operator's OWN organization or declared
  estate — the package is the deliverable, not a threat.
- **Evidence chain per finding.** Every register entry: source finding ID → reach
  proof (read-only) → sensitivity class → valuation → disclosure trigger. No entry
  without a source finding; a harvest claim sourced to nothing is a fabrication.

## The Harvest Loop

```
ingest CONFIRMED findings/chains (3AM state · case files · ledgers)
→ per-finding reach inventory (read-only proofs, ≤3 redacted samples)
→ crown register (what · where · how many · sensitivity class)
→ valuation (tier ladder, ESTIMATE ranges)
→ disclosure map (regulator · timeline · scope · prerequisites)
→ SHUKAKU report (the business-impact verdict layer) → P5 closeout
```

Every ingested finding is either harvested (register entry) or explicitly excluded
with a reason (no data reach, out of scope, wall).

## Working with the chain

The trio runs one engagement as a relay:
- **HolyShit searches** — recon + discovery, confirms targets exist.
- **3AM attacks** — valid attack plans, decisive tests, certification `A→B→C:TAKEOVER`.
- **SHUKAKU harvests** — for each certified finding: reach, price, disclose.
- **KAIRO** supplies hardware-plane findings (device data, keys) into the register.

Output format per crown entry (the deliverable standard):

```
SOURCE: <finding ID / chain>        PROOF: <read-only reach proof, ref>
ASSET: <table/bucket/export/tenant> SCOPE: <rows/records/keys — count*, not contents>
CLASS: <PII|FIN|CRED|BACKUP|SRC|SASS> VALUE: <$ESTIMATE-range + basis>
DISCLOSE: <regulator> · <timeline> · <prerequisite>
```

## Walls (family canon)

- No data movement, no exfiltration, no copying. Catalog-only.
- No weapon authoring, no destruction, no persistence — SHUKAKU inherits all family
  walls; it adds the strictest one: **the harvest register contains descriptions and
  counts, never corpora.**
- Never social. Disclosure packages are deliverables, not threats.
- Findings decay: re-verify reach (3AM `drift`) before re-asserting any price or
  scope.

## Tooling

`scripts/shukaku.py` — stdlib CLI:
- `ingest --target <campaign> --finding "<id>" --proof "<read-only proof ref>"`
- `crown --target <t> --asset "<table|bucket|export>" --class PII|FIN|CRED|BACKUP|SRC|SASS --scope "<count, not contents>" --value "$range" [--basis "..."]`
- `disclose --target <t> --add "<regulator|obligation> · <timeline> · <prerequisite>"`
- `report --target <t> [--output F]` — the harvest deliverable
- `verify` — self-check

State: `~/.redteam/campaigns/<campaign>/harvest-state.json`.

## Files

- `SKILL.md` — this doctrine
- `references/harvest-playbook.md` — catalog/valuation/disclosure batteries + evidence-chain rules
- `scripts/shukaku.py` — ingest/crown/disclose/report/verify CLI
- `templates/harvest-state.json` — per-campaign state starter

## Relations

- `holyshit-mode` — the searcher (discovery + case canon).
- `3am-shinjitsu` — the attacker (findings + chains are SHUKAKU's input).
- `kairo` — the metal (hardware-plane findings feed the register).
- Tree: HolyShit (searcher) · 3AM (attacker) · SHUKAKU (harvester) · KAIRO (metal —
  support branch). All offensive, one gate, catalog-only harvest.