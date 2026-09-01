from pathlib import Path

PROJECT_DOCS = {
    "SRS.md": """# Software Requirements Specification

# Compliance Intelligence Platform

Version: 0.1

Status: Draft

---

This document describes the functional and non-functional requirements
for the Compliance Intelligence Platform.
""",

    "ARCHITECTURE.md": """# System Architecture

The Compliance Intelligence Platform follows a modular ETL architecture.

Collectors
↓

Normalizer
↓

Deduplicator
↓

Database
↓

REST API
↓

Web Interface
""",

    "DATABASE_DESIGN.md": """# Database Design

This document will describe the SQLite schema used by the platform.
""",

    "ROADMAP.md": """# Product Roadmap

## Version 0.1
- Repository
- Documentation
- Database

## Version 0.2
- Presidency Collector

## Version 0.3
- Parliament Collector

## Version 0.4
- Judiciary

## Version 1.0
- Production Release
""",

    "BACKLOG.md": """# Product Backlog

| ID | Task | Status |
|----|------|--------|
| CIP-001 | Database Schema | Pending |
| CIP-002 | Presidency Collector | Pending |
| CIP-003 | Parliament Collector | Pending |
""",

    "CHANGELOG.md": """# Changelog

## v0.1.0

- Initial repository
- Documentation
""",

    "SOURCE_REGISTRY.md": """# Source Registry

| Source | Status |
|--------|--------|
| Presidency | Pending |
| Parliament | Pending |
| Senate | Pending |
| Judiciary | Pending |
"""
}

docs = Path("docs")
docs.mkdir(exist_ok=True)

for filename, content in PROJECT_DOCS.items():

    file = docs / filename

    if not file.exists() or file.stat().st_size == 0:

        file.write_text(content, encoding="utf-8")

        print(f"Created {filename}")

    else:

        print(f"Skipped {filename}")

print("\nProject bootstrap complete.")
