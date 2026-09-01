# Article Implementation

> **Status:** In Progress
> **Project:** Compliance Intelligence Platform
> **Implementation Area:** National Assembly Data Integration
> **Source:** Parliament of Kenya
> **Last Updated:** 2026-09-01

---

## 1. Overview

The Compliance Intelligence Platform is being designed to collect, process, normalize, analyze, and expose compliance-relevant information from authoritative public sources.

One planned source is the Parliament of Kenya, specifically publicly available National Assembly information.

This document records the implementation approach, discoveries, engineering decisions, and remaining work for this integration.

---

## 2. Objective

The objective is to build a reliable ingestion pipeline capable of collecting publicly available parliamentary information and transforming it into structured data that can be consumed by the Compliance Intelligence Platform.

The eventual pipeline should support:

* Source discovery
* Data retrieval
* HTML/API extraction
* Data normalization
* Validation
* Deduplication
* Persistence
* Change detection
* Auditability
* Downstream compliance intelligence

---

## 3. Current Source

The initial source being investigated is the official Parliament of Kenya website.

The National Assembly member directory was successfully retrieved during the initial investigation.

Downloaded HTML snapshots included pages titled:

`Members of National Assembly | The Kenyan Parliament Website`

The retrieved files were inspected for Cloudflare-related failures, and Cloudflare Error 522 was not identified in the inspected snapshots.

---

## 4. Current Discovery

Two major categories of responses were identified.

### 4.1 Member Directory Pages

These responses contained the title:

`Members of National Assembly | The Kenyan Parliament Website`

Several of these files were approximately 239–241 KB.

These are currently considered the most promising source snapshots for member extraction.

### 4.2 Generic Parliament Pages

Other responses contained:

`Parliament of Kenya | The Kenyan Parliament Website`

These files were approximately 106–108 KB.

These appear to represent the broader Parliament website rather than the National Assembly member directory.

---

## 5. Snapshot Duplication

Multiple files representing related requests were produced during the crawling process.

Examples include:

* `national_assembly_1.html`
* `national_assembly_1_<hash>.html`
* `national_assembly_2.html`
* `national_assembly_2_<hash>.html`

The hash-suffixed files appear to represent separate snapshots generated during retrieval.

The production ingestion pipeline should eventually use deterministic deduplication based on factors such as:

* Canonical URL
* Source identifier
* Content hash
* Retrieval timestamp
* Page identifier

---

## 6. Implementation Status

### Completed

* [x] Identified Parliament of Kenya as a potential authoritative source
* [x] Identified the National Assembly member directory
* [x] Successfully retrieved HTML responses
* [x] Inspected retrieved HTML
* [x] Confirmed that inspected responses were not Cloudflare Error 522 pages
* [x] Identified multiple page/snapshot variants
* [x] Identified the need for deterministic deduplication

### In Progress

* [ ] Determine the exact HTML structure containing member records
* [ ] Determine whether member data is embedded directly in HTML
* [ ] Identify any underlying API/data endpoint if applicable
* [ ] Build the Parliament source adapter
* [ ] Normalize member records
* [ ] Validate extracted records
* [ ] Implement deduplication
* [ ] Persist normalized records
* [ ] Implement source change detection
* [ ] Add automated tests
* [ ] Integrate with the broader intelligence pipeline

---

## 7. Planned Data Model

The final schema will depend on the structure and semantics of the source data.

The expected normalized representation may include:

```text
Member
├── id
├── full_name
├── constituency
├── county
├── political_party
├── parliamentary_role
├── committee_memberships
├── source_url
├── source_identifier
├── retrieved_at
├── first_seen_at
├── last_seen_at
└── content_hash
```

Fields should only be populated when supported by authoritative source data.

The system should not invent or infer information that cannot be validated.

---

## 8. Source Adapter Architecture

The Parliament integration should be implemented as a dedicated source adapter.

```text
Parliament Source
       │
       ▼
Parliament Adapter
       │
       ▼
Raw Document
       │
       ▼
Parser
       │
       ▼
Normalizer
       │
       ▼
Validator
       │
       ▼
Deduplicator
       │
       ▼
Compliance Intelligence Data Model
```

This allows Parliament-specific acquisition logic to remain isolated from the rest of the platform.

---

## 9. Data Quality Requirements

The final implementation should prioritize data quality over extraction volume.

Records should ideally be:

* Traceable to their source
* Validated
* Normalized consistently
* Deduplicated
* Timestamped
* Reproducible
* Auditable

Source provenance should be retained so that individual records can be traced back to their origin.

---

## 10. Change Detection

The future implementation should detect changes to parliamentary records.

Conceptually:

```text
Previous Record
      │
      ▼
Content Hash
      │
      ├── Same ──► No Change
      │
      └── Different
              │
              ▼
        Record Changed
              │
              ▼
        Store New Version
```

This would allow the platform to support continuous intelligence collection rather than one-time scraping.

---

## 11. Compliance and Ethical Considerations

The integration is intended to process publicly available institutional information.

The implementation should:

* Respect applicable laws and regulations
* Respect website terms and access policies
* Avoid unnecessary request volume
* Avoid bypassing access controls
* Avoid collecting unnecessary personal information
* Maintain source attribution
* Preserve provenance
* Maintain appropriate audit trails

Official and authoritative sources should be preferred whenever available.

---

## 12. Temporary Implementation Decision

The Parliament extraction work is being documented rather than allowed to block development of the broader platform.

This is an intentional engineering decision.

The core Compliance Intelligence Platform should first establish its:

* Domain model
* Ingestion architecture
* Persistence layer
* Validation layer
* API
* Testing strategy
* Observability
* Documentation
* Deployment structure

Once these components are sufficiently stable, the Parliament integration can be completed as a source-specific adapter.

This prevents the broader platform from becoming tightly coupled to the implementation details of a single website.

---

## 13. Completion Criteria

The Parliament integration will be considered complete when:

* [ ] The official source can be retrieved reliably
* [ ] Member records can be extracted reliably
* [ ] Extraction failures are detectable
* [ ] Records are normalized
* [ ] Records are validated
* [ ] Duplicate records are removed
* [ ] Source provenance is retained
* [ ] Changes can be detected
* [ ] Historical versions can be maintained where appropriate
* [ ] Automated tests cover the parser
* [ ] Integration tests cover the ingestion pipeline
* [ ] Failure and retry behavior is documented
* [ ] The integration works with the production architecture
* [ ] The implementation is sufficiently documented for another developer to maintain

---

## 14. Engineering Principle

The objective is not to build a scraper that merely works once.

The objective is to build a maintainable ingestion component capable of operating as part of a larger compliance intelligence system.

> **Reliability, provenance, maintainability, and data quality take priority over simply extracting the largest possible number of records.**

---

## 15. Future Work

Potential future improvements include:

* Automated scheduled ingestion
* Incremental updates
* Historical record tracking
* Source health monitoring
* Extraction failure alerts
* Data quality metrics
* Cross-source entity resolution
* Entity relationship mapping
* Compliance risk indicators
* Search and investigation workflows

---

## 16. Implementation Log

### 2026-09-01

Initial Parliament source investigation completed.

The National Assembly member directory was successfully retrieved and inspected.

Multiple HTML snapshots were produced during the crawling process. The retrieved files include both National Assembly member-directory pages and generic Parliament pages.

Cloudflare Error 522 was not identified in the inspected snapshots.

Further investigation is required to determine the exact structure of the member records and whether the directory relies on an underlying data endpoint.

The integration has been deliberately documented and deferred so that development of the core Compliance Intelligence Platform can continue without losing the work already completed.

---

## 17. Final Integration Goal

The intended architecture is:

```text
Official Public Source
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

This document will be updated as the implementation progresses.

---

**Status: IN PROGRESS**
