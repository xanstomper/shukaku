<div align="center">

```
   ███╗   ███╗███████╗██╗  ██╗ █████╗ ██╗  ██╗ █████╗ ██╗  ██╗
   ████╗ ████║██╔════╝██║ ██╔╝██╔══██╗██║ ██╔╝██╔══██╗██║ ██╔╝
   ██╔████╔██║█████╗  █████╔╝ ███████║█████╔╝ ███████║█████╔╝
   ██║╚██╔╝██║██╔══╝  ██╔═██╗ ██╔══██║██╔═██╗ ██╔══██║██╔═██╗
   ██║ ╚═╝ ██║███████╗██║  ██╗██║  ██║██║  ██╗██║  ██║██║  ██╗
   ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
```

# 🏺 SHUKAKU

### *Catalog · price · disclose — what an attacker could actually take.*

**The Harvest Mandate of the HolyShit family** — post-compromise data validation,
valuation, and disclosure. It turns 3AM's compromises from technical findings into
**business verdicts**: tables, rows, records, keys, and dollars — priced the way the
extortion market does, packaged the way the law demands. **Without moving a single row.**

[![Version](https://img.shields.io/badge/version-1.1.0-blueviolet?style=for-the-badge)](#the-cli)
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

### The harvest loop

```
ingest CONFIRMED findings/chains (3AM state · case files · ledgers)
→ per-finding reach inventory (read-only proofs, ≤3 redacted samples)
→ crown register (what · where · how many · sensitivity class)
→ valuation (tier ladder, ESTIMATE ranges)
→ disclosure map (regulator · timeline · scope · prerequisites)
→ SHUKAKU report (the business-impact verdict layer) → P5 closeout
```

Every ingested finding is either harvested (crown entry) or **explicitly excluded
with a reason** — never padded.

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
shukaku crown  --target $T --asset users --class PII --scope "12,140 rows" --source "3AM-CHAIN7:TAKEOVER"
shukaku disclose --target $T --trigger PII-EU
shukaku report --target $T --output harvest.md
```

## The CLI

| Command | What it does |
|---|---|
| `ingest --target C --finding ID --proof REF` | ingest a confirmed finding (read-only proof ref) |
| `crown --target C --asset A --class K --scope S --source ID [--value V] [--basis B]` | register a crown entry — evidence-chain enforced, ladder-priced |
| `exclude --target C --finding ID --reason R` | exclude a finding with a reason — never padded |
| `disclose --target C --trigger T [--note N]` \| `--add "…"` | map a disclosure obligation from the playbook |
| `ladder [--class K]` | the valuation ladder + disclosure map |
| `report --target C [--output F]` | the harvest deliverable: crown standard, valuation summary, remediation prerequisites, integrity warnings |
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
│   └── shukaku.py                  # ingest · crown · exclude · disclose · ladder · report · verify
├── references/
│   └── harvest-playbook.md         # catalog/valuation/disclosure batteries + evidence-chain rules
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
