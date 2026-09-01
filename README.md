# Compliance Intelligence Platform

An extensible data intelligence platform for collecting, normalizing, 
resolving, validating, and analyzing publicly available institutional 
information.

> **Status:** Active Development
> **Current Focus:** National Assembly Data Integration
> **Primary Source:** Parliament of Kenya

---

## Overview

The Compliance Intelligence Platform is a modular data-ingestion and 
intelligence system designed to transform publicly available institutional 
information into structured, traceable, and reusable data.

The platform is being developed with a strong emphasis on:

* Reliable data acquisition
* Structured data extraction
* Data normalization
* Entity resolution
* Duplicate detection and merging
* Source provenance
* Validation
* Auditability
* Modular architecture
* Testability
* Maintainability

The initial implementation focuses on integrating publicly available 
information from the Parliament of Kenya, beginning with National Assembly 
member data.

---

## Architecture

The platform follows a modular ingestion architecture:

```text
Authoritative Source
        │
        ▼
Crawler / Collector
        │
        ▼
Raw Source Document
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
Merger / Deduplicator
        │
        ▼
Validator
        │
        ▼
Repository / Database
        │
        ▼
Structured Intelligence Data
```

The architecture is intentionally source-agnostic so that additional 
institutional sources can be integrated without tightly coupling the core 
platform to a single website.

---

## Current Implementation

The repository currently contains the foundations of the platform, 
including:

* Source collectors
* Browser-based collection support
* Pagination handling
* URL discovery
* HTML parsers
* Data models
* Repository abstractions
* Persistence services
* Source-document tracking
* Source-run tracking
* Ingestion pipeline infrastructure
* Entity and relationship resolution components
* Pipeline validation infrastructure
* Automated tests
* Technical documentation foundation

The current source integration work is focused on the Parliament of Kenya 
and its National Assembly member directory.

The Parliament integration has already undergone source discovery and HTML 
inspection. The remaining work involves completing reliable member 
extraction, normalization, validation, deduplication, persistence, and 
source change detection.

The detailed implementation record is maintained in:

`docs/Article_Implementation.md`

---

## Project Structure

```text
Compliance-Intelligence-Platform/
│
├── collectors/       Source acquisition and collection logic
├── crawler/          Crawling and URL discovery
├── parsers/          Source document parsing
├── cleaners/         Data cleaning and normalization
├── resolvers/        Entity and relationship resolution
├── mergers/          Record merging and deduplication
├── models/           Domain models
├── loaders/          Repository and persistence abstractions
├── database/         Database schema and persistence infrastructure
├── pipeline/         Ingestion pipeline orchestration
├── services/         Application services
├── config/           Configuration and source definitions
├── utils/            Shared utilities and logging
├── tools/            Investigation and source-discovery tools
├── docs/             Architecture and engineering documentation
│
├── main.py           Application entry point
├── app.py            Application interface
├── requirements.txt  Python dependencies
└── README.md         Project documentation
```

---

## Engineering Principles

The platform is being developed around several core principles.

### Source Provenance

Data should remain traceable to the authoritative source from which it was 
obtained.

### Deterministic Processing

Where possible, ingestion and transformation should produce predictable 
and reproducible results.

### Separation of Concerns

Source-specific acquisition logic should remain separate from parsing, 
normalization, resolution, persistence, and downstream intelligence.

### Data Quality

Extraction volume is secondary to correctness, validation, traceability, 
and consistency.

### Maintainability

The system should be understandable and extensible by another developer 
without requiring knowledge of the original implementation process.

### Auditability

Important source and processing information should be retained so that 
data transformations can be investigated when necessary.

---

## Testing

The project includes automated tests covering multiple parts of the 
ingestion architecture, including:

* Crawling
* Source discovery
* Collectors
* Parsers
* Pagination
* Repositories
* Source documents
* Ingestion pipelines

Tests can be run with:

```bash
pytest
```

---

## Documentation

Technical documentation is maintained under `docs/`.

Important documents include:

* `ARCHITECTURE.md` — System architecture
* `DATABASE_DESIGN.md` — Database design
* `SRS.md` — Software requirements specification
* `ROADMAP.md` — Development roadmap
* `BACKLOG.md` — Outstanding work
* `CHANGELOG.md` — Development history
* `SOURCE_REGISTRY.md` — Source registry documentation
* `Article_Implementation.md` — Detailed Parliament integration 
investigation and implementation record

---

## Current Development Status

The platform is actively under development.

### Core Platform

* [x] Modular project structure
* [x] Domain models
* [x] Repository layer
* [x] Database infrastructure
* [x] Ingestion pipeline foundation
* [x] Collector abstractions
* [x] Parser abstractions
* [x] Source document tracking
* [x] Source run tracking
* [x] Automated test suite foundation
* [x] Technical documentation

### Parliament of Kenya Integration

* [x] Identified authoritative source
* [x] Discovered National Assembly member directory
* [x] Retrieved source HTML
* [x] Inspected source responses
* [x] Investigated source variations
* [x] Documented engineering findings
* [ ] Complete member extraction
* [ ] Normalize member records
* [ ] Validate extracted records
* [ ] Implement deterministic deduplication
* [ ] Persist normalized records
* [ ] Implement change detection
* [ ] Complete integration testing
* [ ] Finalize production integration

The incomplete Parliament integration is intentionally documented rather 
than hidden. The implementation record is maintained in 
`docs/Article_Implementation.md` so that the work, discoveries, and 
engineering decisions remain available for continued development.

---

## Data Sources

The platform is designed to prioritize authoritative public sources.

The initial integration work uses publicly available information from the 
Parliament of Kenya.

Future integrations may include additional institutional sources where 
appropriate and legally permissible.

---

## Compliance and Responsible Data Use

The platform is intended to process publicly available institutional 
information.

Development principles include:

* Respecting applicable laws and regulations
* Respecting source access policies
* Avoiding unnecessary request volume
* Avoiding attempts to bypass access controls
* Minimizing unnecessary personal information
* Maintaining source attribution
* Preserving provenance
* Maintaining appropriate audit trails

---

## Technology

The current implementation is primarily Python-based and uses a modular 
architecture designed around:

* Python
* HTML parsing
* Web data collection
* SQLite/database persistence
* Automated testing
* Modular service and repository patterns

Specific dependencies are maintained in `requirements.txt`.

---

## Development Philosophy

This project is not intended to be a one-off scraper.

The goal is to build a maintainable data-ingestion and intelligence 
platform capable of incorporating multiple authoritative sources while 
preserving provenance, data quality, and architectural separation.

The long-term direction is:

```text
Authoritative Sources
        ↓
Reliable Acquisition
        ↓
Raw Data Preservation
        ↓
Extraction
        ↓
Normalization
        ↓
Validation
        ↓
Deduplication
        ↓
Entity Resolution
        ↓
Compliance Intelligence
        ↓
API / Search / Analysis
```

---

## Project Status

**Active Development**

The architecture and ingestion foundations are being developed 
incrementally, with the Parliament of Kenya integration serving as the 
first major source-specific implementation.

Detailed implementation decisions and discoveries are documented 
throughout the repository.

