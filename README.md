# Compliance Intelligence Platform

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22232969.svg)](https://doi.org/10.5281/zenodo.22232969)

A citation-backed data intelligence platform for collecting, normalizing,
resolving, validating, and analyzing publicly available institutional
information on Kenya's Politically Exposed Persons (PEPs).

> **Status:** Active dataset, 13 sources integrated
> **Current dataset:** 775 active PEP records, citation-backed, across 14 institutions
> **Primary purpose:** Feeding a Kenya PEP registry into a UN Sanctions Explorer portal

---

## Overview

The Compliance Intelligence Platform is a modular data-ingestion and
intelligence system that transforms publicly available institutional
information into structured, traceable, citation-backed data suitable
for compliance and sanctions-screening use cases.

Every person record in this dataset is backed by at least one citation
row pointing to the literal source document it was extracted from --
no record exists without a traceable origin.

---

## Current Dataset

| Metric | Value |
|---|---|
| Active PEP records | 775 |
| Tombstoned (merged duplicate) records | 2 |
| Citation rows | 775 (1:1 coverage on all active records) |
| Institutions covered | 14 |
| Sources integrated | 13 |

### Sources covered

| Source | Records | Method |
|---|---|---|
| National Assembly | 347 | Playwright (JS-rendered), 36-page crawl |
| High Court | 114 | Plain HTTP |
| Senate | 67 | Plain HTTP, 7-page crawl |
| Environment and Land Court | 62 | Plain HTTP |
| Governors (Council of Governors) | 47 | Plain HTTP, single page |
| Court of Appeal | 41 | Plain HTTP |
| Cabinet | 24 | Plain HTTP |
| Kenya Revenue Authority (KRA) | 20 | Plain HTTP |
| Employment and Labour Relations Court | 17 | Plain HTTP |
| Kenya Power and Lighting Company (KPLC) | 13 | Plain HTTP |
| National Social Security Fund (NSSF) | 8 | Plain HTTP |
| Presidency (Office of the President + Deputy President) | 8 | Plain HTTP, 2 pages |
| Supreme Court | 7 | Plain HTTP |

All five Judiciary court levels (Supreme Court, Court of Appeal, High
Court, Employment and Labour Relations Court, Environment and Land
Court) share a single generic parser (`parsers/judiciary_parser.py`),
since all five use the same underlying WordPress team-member plugin
markup -- only the institution name and job-title phrasing differ,
and the parser normalizes both.

### Known gaps (not sources of failure -- documented scope boundaries)

| Gap | Reason |
|---|---|
| KenGen | Site returns a Cloudflare-style bot-detection challenge page; not reachable via plain HTTP |
| Kenya Pipeline Company (KPC) | Board data loads via a WordPress AJAX/shortcode widget not present in static HTML; would need browser rendering to reach |
| Central Bank of Kenya (CBK) | Site is behind a Sucuri Website Firewall returning HTTP 403 to automated requests |
| Social Health Authority (SHA) | Not yet attempted |
| County Assemblies (all 47) | Each county runs its own separate, structurally inconsistent website; scoped as a future phased rollout (5-county pilot), not started |
| Family members / close associates of PEPs | Not yet started -- requires a higher evidentiary bar per person (2+ independent sources) before inclusion, per the platform's PEP taxonomy |

---

## Architecture

```text
Authoritative Source
        │
        ▼
Crawler / Collector
        │
        ▼
Raw Source Document (immutable, content-addressed HTML snapshot)
        │
        ▼
Parser
        │
        ▼
Cleaner / Normalizer
        │
        ▼
Entity Resolver
        │
        ▼
Merger / Deduplicator (tombstone pattern, audit-trail preserved)
        │
        ▼
Validator
        │
        ▼
Repository / Database (SQLite)
        │
        ▼
Citation Layer (sources table -- every record traceable to its source URL)
        │
        ▼
Export / API Layer
        │
        ▼
UN Sanctions Explorer Integration
```

The architecture is source-agnostic: additional institutional sources
can be integrated without coupling the core platform to any single
website's structure.

---

## Entity Resolution

`tools/find_duplicate_persons.py` performs fuzzy name-similarity
matching (with honorific/suffix normalization) across the full
dataset to surface candidate duplicate person records for human
review. It does not auto-merge anything -- in a compliance context,
a false merge is worse than a missed one.

Two confirmed duplicates have been merged to date, using a tombstone
pattern: the duplicate record's `entity_status` is set to `MERGED`
and `merged_into_person_id` points to the canonical record. Nothing
is ever deleted, preserving full audit trail.

Known limitation: the similarity scoring is bag-of-words based and
produces false positives among people who share common Kenyan or
Somali-Kenyan name components (e.g. "Mohamed", "Abdi", "Joseph") --
these are reviewed and correctly left unmerged. Cross-institution
matches (e.g. an MP name resembling a judge's name) are structurally
implausible given Kenya's separation-of-powers rules and can usually
be dismissed without deep investigation.

---

## Citation / Provenance Layer

Every person record persisted through the pipeline automatically
receives a row in the `sources` table (`loaders/source_repository.py`,
wired into `services/persistence_service.py`), citing:

- `source_name` -- which institution/source produced this record
- `source_url` -- the literal URL of the document it was extracted from
- `trust_score` -- the extraction confidence score
- `collected_at` / `last_verified` -- timestamps

This is distinct from `source_documents` (the raw HTML snapshot audit
log) and `source_runs` (collector execution history) -- the `sources`
table is the compliance-facing citation a human reviewer or the
Sanctions Explorer portal would check to verify a record's origin.

---

## Export & API Layer

- `tools/export_dataset.py` generates a full JSON and CSV export of
  the active dataset (`output/kenya_peps_export.json` /
  `output/kenya_peps_export.csv`), including nested positions and
  citations per person.
- `app.py` exposes a REST API for live querying (see API section
  below / in-code docstrings for endpoint details).

---

## Project Structure

```text
Compliance-Intelligence-Platform/
│
├── collectors/       Source acquisition and collection logic
├── crawler/          Crawling and URL discovery
├── parsers/          Source document parsing
├── cleaners/         Data cleaning and normalization
├── resolvers/        Relationship ID resolution
├── mergers/          Record merging and deduplication (scaffolded)
├── models/           Domain models (Person, Position, Institution, Source, ...)
├── loaders/          Repository and persistence abstractions
├── database/         Database schema and persistence infrastructure
├── pipeline/         Ingestion pipeline orchestration
├── services/         Application services (PersistenceService)
├── config/           Configuration and source definitions
├── utils/            Shared utilities and logging
├── tools/            Investigation, dedup, backfill, and export tools
├── dev_investigation/  One-off structure-inspection scripts from source onboarding
├── docs/             Architecture and engineering documentation
│
├── main.py           Application entry point
├── app.py            REST API (Flask)
├── requirements.txt  Python dependencies
└── README.md         This file
```

---

## Engineering Principles

- **Source Provenance** -- every record traces to its authoritative source (enforced by the citation layer).
- **Deterministic Processing** -- ingestion and transformation are reproducible.
- **Separation of Concerns** -- acquisition, parsing, normalization, resolution, and persistence stay decoupled.
- **Data Quality Over Volume** -- correctness and traceability take priority over record count.
- **Auditability** -- merges are tombstoned, never deleted; every parser fix in this project's history was verified against real fetched HTML before being trusted.

---

## Testing

```bash
pytest
```

---

## Running the Pipeline

Each source has its own collector + parser pair. Example (Cabinet):

```python
from collectors.cabinet_collector import CabinetCollector
from parsers.cabinet_parser import CabinetParser
from pipeline.ingestion_pipeline import IngestionPipeline

pipeline = IngestionPipeline(
    collector=CabinetCollector(),
    parser=CabinetParser()
)
result = pipeline.run()
pipeline.close()
```

To regenerate the full export:

```bash
python tools/export_dataset.py
```

To scan for duplicate records:

```bash
python tools/find_duplicate_persons.py
```

---

## Compliance and Responsible Data Use

This platform processes publicly available institutional information
only. Development principles include respecting source access
policies, avoiding unnecessary request volume, minimizing unnecessary
personal information, maintaining source attribution, and preserving
full provenance and audit trails throughout.

---

## Publication

**DOI:** https://doi.org/10.5281/zenodo.22232969
**Repository:** https://github.com/saint-art/Compliance-Intelligence-Platform

---

## License

MIT
