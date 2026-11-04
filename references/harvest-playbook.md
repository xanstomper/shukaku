# SHUKAKU — Harvest Playbook (catalog · price · disclose)

The deliverable is a register of what an attacker could take — descriptions and
counts, never corpora. Every entry chains to a source finding; every price is an
ESTIMATE range with a basis; every disclosure trigger names the obligation.

## Phase 1 — Catalog (reach inventory, read-only)

| Asset class | Reach proof (read-only) | Registered scope |
|---|---|---|
| SQL DB | `SELECT count(*) FROM <table>` with harvested creds | table · row count · schema classes |
| NoSQL | `db.<col>.count()` (operator-owned) | collection · doc count |
| Object store | bucket listing + key count | bucket · key count · prefixes |
| Backups | backup inventory list (glacier/S3/cron/NFS) | artifact · size · freshness |
| SaaS export | tenant admin export config review (read-only list) | tenant · export scope |
| Source repos | repo list + secret scan (operator-owned code) | repos · secret class counts |
| Device/keys | KAIRO findings: key extraction proof (read-only) | key material type · count |

Sample rule: ≤3 rows, redacted at capture, only to prove class — the register keeps
counts and hashes of samples, never contents.

## Phase 2 — Valuation (the extortion-economy ladder)

ESTIMATE ranges per record/asset, labeled with basis. Prices are ranges, never false
precision:

| Class | Basis (observed market) | Range (ESTIMATE) |
|---|---|---|
| PII — US consumer | ~$5–15/record street, breach-class aggregation multipliers | per 1k rows |
| PII — EU (GDPR-class) | higher penalty-weight, lower street | per 1k rows |
| FIN (cards/banking) | $20–50/record class | per record |
| CRED (secrets/keys) | credential-market tiers by privilege | per credential |
| BACKUP (unencrypted dump) | lump: % of org revenue-class (ransom demand logic) | per artifact |
| SRC (exclusive repo) | private repo market + IP class | per repo |
| SASS (tenant export) | SaaS-resale/takeover ladder | per tenant |

Valuation MUST be labeled: `$ESTIMATE (basis: <market-ladder | disclosed demand |
industry benchmark>)`. No invented precision; a single-number price without basis
is a violation.

## Phase 3 — Disclosure map

| Trigger | Obligation class | Timeline class | Prerequisite |
|---|---|---|---|
| PII breached (US/state) | state AG notification laws | 30d class | investigation complete |
| PII breached (EU) | GDPR Art. 33/34 | 72h class | risk assessment |
| FIN/PCI | card-brand + acquiring bank | immediate class | forensic report |
| Health | HIPAA/HITECH HHS | 60d class | risk assessment |
| Corporate secrecy | contracts/insurance breach clauses | policy class | legal review |
| Backup/ransom-class | extortion-reporting + regulator | 24h class | containment |

The map is a DELIVERABLE for the operator's own org — it names what the company
would owe, it is never used to threaten anyone.

## Evidence-chain rules

1. Every crown entry: `SOURCE → PROOF → SCOPE → CLASS → VALUE → DISCLOSE`.
2. SOURCE must be a real finding ID (3AM chain, case file, ledger entry) — a harvest
   entry with no source is a fabrication.
3. PROOF must be reproducible read-only (command ref, output hash reference).
4. SCOPE is counts, never contents; samples ≤3, redacted, hashed.
5. VALUE carries basis; DISCLOSE carries the obligation + timeline + prerequisite.
6. Re-verify reach before re-asserting (drift first; findings decay).

## Negatives & closeout

- A finding with no data reach is EXCLUDED with the reason, not padded.
- The SHUKAKU report is the P5 impact layer: register + valuation summary +
  disclosure map + remediation prerequisites (what must happen before the
  organization can call the breach closed).
- Never move data, never copy, never threaten. The register IS the harvest.

## The hunt batteries (v1.2 — the harvester hunts)

### Signal → harvestable plane (the reasoning table)

`reason` matches confirmed access against these signals; each hit becomes a ranked
hypothesis with the exact read-only proof:

| Signal (regex on findings/proofs/ledgers) | Plane | Class | Read-only proof |
|---|---|---|---|
| sql / database / select count | SQL plane | PII | `information_schema.tables` + row counts |
| s3 / bucket / object store / minio | object storage | BACKUP | bucket key inventory + prefixes |
| admin / tenant / saas / export | SaaS admin | SASS | export-config list + member counts |
| repo / source / github | source plane | SRC | repo list + secret-class counts |
| ssh / shell / root / host | host filesystem | CRED | env/cron/keyfile listings (counts) |
| key / secret / token / firmware | keyring/device | CRED | keyring + cert inventories |
| http / url / api / endpoint | harvest surface | BACKUP | GET-only surface probe |
| registered crowns | drift | (same) | re-run the reach proof |

### The harvest surface (GET-only, `hunt --live`)

backup archives (`backup.zip|tar.gz|sql`, `dump.sql`, `db.sqlite`…), env/config
leaks (`.env`, `.git/config`, `config.*.bak`), admin/admin-export paths,
`api/export(s)`, `debug/vars`, `server-status`. Data plane only — route probing is
UNDERCROFT's. 200s register CONFIRMED with body sizes; **nothing is downloaded**.

### The feed mappings (discovery → family material)

| Discovery | → 3AM row (flaw · seam) | → undercroft | → holyshit |
|---|---|---|---|
| exposed backup/dump (hunt or BACKUP crown) | 13 cloud-misconfig · K cloud-policy | — | recipe card |
| exposed .env/.git/config | 15 database-exposure · G edgefn<->db | CONFIRMED surface | recipe card |
| admin/export reach (SASS crown) | 6 identifier-trust · C auth<->backend-binding | CONFIRMED surface (admin) | — |
| data plane via harvested access (PII/FIN crown) | 15 database-exposure · G edgefn<->db | — | — |
| SRC crown | 2 trust-in-client-params · B client<->server-validation | — | recipe card |
| CRED crown | 10 entropy/forge · C auth<->backend-binding (reuse check) | — | — |

Feed is idempotent per (kind, what, destination) — never double-shipped. Next
steps after feed: `3AM promote --apply --verified` · `kairo ingest --target <t>`.