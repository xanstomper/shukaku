<div align="center">

```

```

# 🏺 SHUKAKU

### *Reason · hunt · crown · price · disclose — then feed the family.*

**The Harvest Mandate of the HolyShit family** — the harvester. It REASONS about
what should be harvestable from confirmed access, HUNTS for it (read-only), prices
it the way the extortion market does, builds the breach-disclosure package — and
**feeds every discovery back to the other mandates so the next assault is stronger.**
Without moving a single row.

[![Version](https://img.shields.io/badge/version-1.2.0-blueviolet?style=for-the-badge)](#the-cli)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#quickstart)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#quickstart)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge)](#why-its-powerful)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![CI](https://github.com/xanstomper/shukaku/actions/workflows/verify.yml/badge.svg)](https://github.com/xanstomper/shukaku/actions/workflows/verify.yml)
[![Use](https://img.shields.io/badge/use-AUTHORIZED%20TARGETS%20ONLY-crimson?style=for-the-badge)](#the-walls-non-negotiable)

**THE FAMILY** — six siblings and the dispatcher, one click each:

[![00 BARBICAN · the shield](https://img.shields.io/badge/00-BARBICAN%20·%20the%20shield-2E4057?style=for-the-badge)](https://github.com/xanstomper/barbican)
[![01 3AM · the performer](https://img.shields.io/badge/01-3AM%20·%20the%20performer-8B0000?style=for-the-badge)](https://github.com/xanstomper/3am-shinjitsu)
[![02 KAIRO · the synthesizer](https://img.shields.io/badge/02-KAIRO%20·%20the%20synthesizer-6B8E23?style=for-the-badge)](https://github.com/xanstomper/kairo)
[![03 UNDERCROFT · the descent](https://img.shields.io/badge/03-UNDERCROFT%20·%20the%20descent-4B0082?style=for-the-badge)](https://github.com/xanstomper/undercroft)
[![04 HOLYSHIT · the finder](https://img.shields.io/badge/04-HOLYSHIT%20·%20the%20finder-B8860B?style=for-the-badge)](https://github.com/xanstomper/HolyShit)
[![05 SHIKI · the command](https://img.shields.io/badge/05-SHIKI%20·%20the%20command-111111?style=for-the-badge)](https://github.com/xanstomper/shiki)
[![SPYDERMONKEY · the dispatcher](https://img.shields.io/badge/🕷️-SPYDERMONKEY%20·%20the%20dispatcher-blueviolet?style=for-the-badge)](https://github.com/xanstomper/spydermonkey)

[How it works](#how-it-works) · [Why it's powerful](#why-its-powerful) ·
[Quickstart](#quickstart) · [The CLI](#the-cli) · [The Walls](#the-walls-non-negotiable)

</div>

---

## What is this?

HolyShit **searches**, 3AM **attacks** — SHUKAKU **harvests**. It answers the only
question the family's verdicts exist for:

> **What did the attacker actually GAIN — in tables, rows, records, keys, and
> dollars — and who must be told?**

The cartel economy runs on data. SHUKAKU catalogs what a confirmed compromise makes
reachable (**without moving a single row**), prices it the way the extortion market
does, and builds the breach-disclosure package the operator's own organization would
owe. It is the P4→P5 completing role: the closeout's impact layer.

## How it works

### The harvest loop — it closes

```
ingest CONFIRMED findings/chains (3AM state · case files · ledgers)
→ REASON   what SHOULD be harvestable — inferred planes from confirmed access
→ HUNT     read-only proofs: exact static probes or GET-only live surface probes
→ crown register (what · where · how many · sensitivity class)
→ valuation (tier ladder, ESTIMATE ranges)
→ disclosure map (regulator · timeline · scope · prerequisites)
→ FEED the family (3AM vectors · undercroft surface · holyshit recipes → kairo)
→ SHUKAKU report (the business-impact verdict layer) → P5 closeout
```

Every ingested finding is either harvested (crown entry) or **explicitly excluded
with a reason** — never padded. The loop CLOSES: what the harvest learns becomes
attack material the whole family carries.

### The reasoning engine — the harvester hunts

`reason` reads the campaign's confirmed access (ingested findings, undercroft
CONFIRMED seams, kairo device notes) and infers the harvestable planes, ranked by
the ladder:

```
═══ SHUKAKU reason — what SHOULD be harvestable (3 hypotheses) ═══
  H-001 [PII   ] SQL plane        database tables + row counts
         source: 3AM-T1-CHAIN7:TAKEOVER
         probe:  SELECT table_name, table_rows FROM information_schema.tables
  H-002 [BACKUP] harvest surface  exposed dumps/exports/env/config paths
         source: /admin/export
         probe:  GET-only harvest-surface probe (see: hunt --live)
  H-003 [SASS  ] SaaS admin       tenant export inventory + member counts
         source: /admin/export
         probe:  export-config list + member count (read-only)
```

`hunt` works the hypotheses:

- **static** (default) — prints the EXACT read-only proof per hypothesis; nothing
  is executed. Safe by construction.
- **`--live URL`** — GET-only probes of the harvest surface (backup dumps, exports,
  .env/.git paths, admin exports — the data plane, not the route plane):

```
▸ hunt --live: 8 GET-only probes (0.2s pacing, burst pauses) — catalog-only
    HARVESTABLE 200  https://target.example/backup.zip  (4096B)
▸ hunt done: 1 harvestable path(s) confirmed (registered: 1 total)
```

### `feed` — the loop that arms the family

Every crown and CONFIRMED hunt hit becomes family attack material, schema-true
for each consumer:

```
▸ SHUKAKU feeds the family — the next assault starts smarter:
    3AM: 2 vector row(s) → ~/.redteam/learned-vectors.jsonl
    undercroft: 1 CONFIRMED surface entry → the campaign ledger
    holyshit: 1 recipe card(s) → ~/.redteam/synthesized-recipes.md
  next: 3AM promote --apply --verified · kairo ingest --target t3
```

Exposed backup → 3AM flaw 13 (cloud-misconfig) · seam K (cloud-policy). Exposed
.env/.git → flaw 15 (database-exposure) · seam G (edgefn<->db). The sweep picks
them up on the next campaign — fed rows are recorded, **never double-shipped**.

### The evidence chain — enforced, not aspirational

```
$ shukaku crown --target t1 --asset users --class PII --scope "12k rows"
✗ --source required: a harvest entry with no source is a fabrication
  — ingest the finding first          # rc=2

$ shukaku crown --target t1 --asset users --class PII --scope "12,140 rows" \
      --source "3AM-T1-CHAIN7:TAKEOVER" --value "1.2M"
✗ value must be labeled $ESTIMATE — a single-number price without basis is a
  violation (see: shukaku ladder)     # rc=2

$ shukaku crown --target t1 --asset users --class PII --scope "12,140 rows" \
      --source "3AM-T1-CHAIN7:TAKEOVER"
▸ crown: crown-001 users [PII] 12,140 rows — $5,000–15,000 ESTIMATE (per 1k rows)
```

- **No source, no crown.** Every entry chains to a real ingested finding ID; the
  CLI refuses fabrications.
- **No invented precision.** Values must carry an ESTIMATE label — omit `--value`
  and the ladder prices it for you, with its market basis attached.

### The valuation ladder (playbook canon)

```
$ shukaku ladder
═══ SHUKAKU valuation ladder — ESTIMATE ranges, never invented precision ═══
  PII    PII — US consumer             per 1k rows       $5,000–15,000 ESTIMATE
         basis: ~$5–15/record street; breach-class aggregation multipliers apply
  PII    PII — EU (GDPR-class)         per 1k rows       lower street, higher penalty-weight ESTIMATE
         basis: GDPR penalty economics shift value from resale to liability
  FIN    FIN — cards/banking           per record        $20–50 ESTIMATE
  CRED   CRED — secrets/keys           per credential    tiered by privilege ESTIMATE
  BACKUP BACKUP — unencrypted dump     per artifact      % of org revenue-class ESTIMATE
  SRC    SRC — exclusive repo          per repo          private-repo market + IP class ESTIMATE
  SASS   SASS — tenant export          per tenant        resale/takeover ladder ESTIMATE

═══ disclosure map — what a breached org would owe ═══
  PII-US    state AG notification laws             30d class        prereq: investigation complete
  PII-EU    GDPR Art. 33/34                        72h class        prereq: risk assessment
  FIN       card brands + acquiring bank           immediate class  prereq: forensic report
  HEALTH    HIPAA/HITECH — HHS                     60d class        prereq: risk assessment
  CONTRACT  contracts/insurance breach clauses     policy class     prereq: legal review
  RANSOM    extortion-reporting + regulator        24h class        prereq: containment
```

## Why it's powerful

- **The harvester hunts.** It doesn't wait to be told what exists — `reason`
  infers the harvestable planes from the access the family already proved, ranks
  them by value, and `hunt` goes after them read-only. Confirmed DB access
  *implies* a table inventory; confirmed tenant admin *implies* an export list.
  The harvester names them, then proves them.
- **The loop compounds.** `feed` converts every discovery into attack material the
  whole family carries — 3AM vectors, undercroft CONFIRMED surface, holyshit
  recipes, kairo's queue. The next assault against the target starts smarter, and
  the one after that too.
- **The verdict layer.** Every other mandate proves what's *possible*; SHUKAKU
  proves what's *worth* — and turns the proof into the disclosure obligations a
  real breach would trigger. That's the difference between a pentest report and a
  business verdict.
- **Catalog, never collect.** Reach is proven read-only: `SELECT count(*)`, bucket
  listings, export inventories. Samples ≤3 rows, redacted at capture. The register
  is the deliverable, **not the data** — nothing is ever moved, copied, or exfiltrated.
- **Market-true pricing.** Valuation tiers mirror the observed extortion economy
  (PII street prices, card-record classes, ransom-demand logic on backups) — with
  bases labeled, ranges not numbers.
- **The map is the deliverable.** The disclosure map names regulator obligations,
  notification timelines, affected scope, and remediation prerequisites for the
  operator's OWN organization — it is a compliance artifact, never a threat.
- **Fabrication-proof.** The evidence chain (SOURCE → PROOF → SCOPE → CLASS →
  VALUE → DISCLOSE) is enforced in code: unsourced entries refuse, precision-less
  prices refuse, unharvested findings surface as integrity warnings in the report.
- **Zero dependencies.** Pure Python stdlib, one file. Clone and run.

## Quickstart

```bash
git clone https://github.com/xanstomper/shukaku.git
python3 shukaku/scripts/shukaku.py ladder                  # the ladder + disclosure map
python3 shukaku/scripts/shukaku.py verify                  # self-check

# as a Hermes skill (where the family lives)
git clone https://github.com/xanstomper/shukaku.git \
    ~/.hermes/skills/security/shukaku
```

Typical run on a declared estate:

```bash
T=my-campaign
shukaku ingest --target $T --finding "3AM-CHAIN7:TAKEOVER" --proof "count(*) = 12140"
shukaku reason --target $T                    # what SHOULD be harvestable, ranked
shukaku hunt --target $T                      # exact read-only proofs (static)
shukaku hunt --target $T --live https://t.example --max 30   # GET-only surface probe
shukaku crown  --target $T --asset users --class PII --scope "12,140 rows" --source "3AM-CHAIN7:TAKEOVER"
shukaku disclose --target $T --trigger PII-EU
shukaku feed --target $T                      # 3AM + undercroft + holyshit get stronger
shukaku report --target $T --output harvest.md
```

## The CLI

| Command | What it does |
|---|---|
| `ingest --target C --finding ID --proof REF` | ingest a confirmed finding (read-only proof ref) |
| `reason --target C [--json]` | infer what SHOULD be harvestable from confirmed access → ranked hypotheses |
| `hunt --target C [--live URL] [--max N] [--dry-run]` | work the hypotheses: exact read-only proofs (static) or GET-only harvest-surface probes (live, catalog-only) |
| `crown --target C --asset A --class K --scope S --source ID [--value V] [--basis B]` | register a crown entry — evidence-chain enforced, ladder-priced |
| `exclude --target C --finding ID --reason R` | exclude a finding with a reason — never padded |
| `disclose --target C --trigger T [--note N]` \| `--add "…"` | map a disclosure obligation from the playbook |
| `feed --target C` | harvest → family: 3AM vectors, undercroft surface, holyshit recipes — idempotent, never double-shipped |
| `ladder [--class K]` | the valuation ladder + disclosure map |
| `report --target C [--output F]` | the harvest deliverable: hypotheses, hunt results, crown standard, valuation, remediation prerequisites, fed-loop, integrity warnings |
| `verify` | self-check |

Exit codes: `0` ok · `1` verify failure · `2` usage/state error (walls).

## The Walls (non-negotiable)

- **No data movement, no exfiltration, no copying. Catalog-only.** The register
  contains descriptions and counts, never corpora.
- Every entry chains to a source finding — a harvest claim sourced to nothing is
  a fabrication and the CLI refuses it.
- No weapon authoring, no destruction, no persistence; all family walls inherited.
- Never social. Disclosure packages are deliverables, not threats.
- Findings decay: re-verify reach before re-asserting any price or scope.

## Files

```
shukaku/
├── SKILL.md                        # the doctrine
├── scripts/
│   └── shukaku.py                  # ingest · reason · hunt · crown · exclude · disclose · feed · ladder · report · verify
├── references/
│   └── harvest-playbook.md         # catalog/valuation/disclosure batteries + evidence-chain rules + hunt batteries
└── templates/
    └── harvest-state.json          # per-campaign state starter
```

## Relations

`spydermonkey` dispatches it · `barbican` gates it · `shiki` conducts it ·
`3am-shinjitsu` feeds it CONFIRMED chains · `kairo` feeds hardware-plane findings ·
`holyshit-mode` finds what's there.

## License

[MIT](LICENSE) — use the harvest, build for it, route through it.

<div align="center">

*The register IS the harvest. Nothing moves.*

</div>
