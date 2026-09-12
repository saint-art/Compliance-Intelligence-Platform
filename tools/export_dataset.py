"""
Exports the full active PEP dataset to JSON and CSV, suitable
for import into the UN Sanctions Explorer or any other
downstream system.

Each person record includes:
  - Core identity fields
  - Their position(s) and institution(s)
  - Full citation trail (source_name, source_url, trust_score)

Excludes tombstoned (MERGED) records -- only active, canonical
persons are exported.

Run:
    python tools/export_dataset.py
"""

import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("database/compliance.db")
OUTPUT_DIR = Path("output")


def fetch_persons_with_positions(conn):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.first_name,
            p.middle_name,
            p.last_name,
            p.gender,
            p.nationality,
            p.country,
            p.date_of_birth,
            p.is_pep,
            p.is_sanctioned,
            p.risk_level,
            p.confidence_score,
            p.primary_source,
            p.entity_status,
            p.political_party,
            p.constituency,
            p.county,
            p.profile_url,
            p.image_url,
            p.status,
            p.created_at,
            p.updated_at,
            pos.title AS position_title,
            pos.category AS position_category,
            inst.institution_name,
            inst.category AS institution_category,
            pp.is_current,
            pp.start_date,
            pp.end_date
        FROM persons p
        LEFT JOIN person_positions pp
            ON pp.person_id = p.person_id
        LEFT JOIN positions pos
            ON pos.position_id = pp.position_id
        LEFT JOIN institutions inst
            ON inst.institution_id = pp.institution_id
        WHERE p.entity_status != 'MERGED'
        ORDER BY p.person_id
        """
    )

    rows = cur.fetchall()

    people = {}

    for row in rows:

        pid = row["person_id"]

        if pid not in people:

            people[pid] = {
                "person_id": pid,
                "full_name": row["full_name"],
                "first_name": row["first_name"],
                "middle_name": row["middle_name"],
                "last_name": row["last_name"],
                "gender": row["gender"],
                "nationality": row["nationality"],
                "country": row["country"],
                "date_of_birth": row["date_of_birth"],
                "is_pep": bool(row["is_pep"]),
                "is_sanctioned": bool(row["is_sanctioned"]),
                "risk_level": row["risk_level"],
                "confidence_score": row["confidence_score"],
                "primary_source": row["primary_source"],
                "entity_status": row["entity_status"],
                "political_party": row["political_party"],
                "constituency": row["constituency"],
                "county": row["county"],
                "profile_url": row["profile_url"],
                "image_url": row["image_url"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "positions": [],
                "sources": []
            }

        if row["position_title"]:

            people[pid]["positions"].append({
                "title": row["position_title"],
                "category": row["position_category"],
                "institution_name": row["institution_name"],
                "institution_category": row["institution_category"],
                "is_current": bool(row["is_current"]),
                "start_date": row["start_date"],
                "end_date": row["end_date"]
            })

    return people


def attach_sources(conn, people):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            person_id,
            source_name,
            source_url,
            source_type,
            trust_score,
            collected_at,
            last_verified
        FROM sources
        ORDER BY person_id
        """
    )

    for row in cur.fetchall():

        pid = row["person_id"]

        if pid in people:

            people[pid]["sources"].append({
                "source_name": row["source_name"],
                "source_url": row["source_url"],
                "source_type": row["source_type"],
                "trust_score": row["trust_score"],
                "collected_at": row["collected_at"],
                "last_verified": row["last_verified"]
            })


def write_json(people, path):

    payload = {
        "export_generated_at": datetime.utcnow().isoformat(),
        "total_records": len(people),
        "persons": list(people.values())
    }

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def write_csv(people, path):

    fieldnames = [
        "person_id", "full_name", "is_pep", "is_sanctioned",
        "risk_level", "confidence_score", "primary_source",
        "political_party", "constituency", "county",
        "position_title", "institution_name",
        "profile_url", "source_url", "entity_status"
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for person in people.values():

            primary_position = (
                person["positions"][0] if person["positions"] else {}
            )
            primary_source_row = (
                person["sources"][0] if person["sources"] else {}
            )

            writer.writerow({
                "person_id": person["person_id"],
                "full_name": person["full_name"],
                "is_pep": person["is_pep"],
                "is_sanctioned": person["is_sanctioned"],
                "risk_level": person["risk_level"],
                "confidence_score": person["confidence_score"],
                "primary_source": person["primary_source"],
                "political_party": person["political_party"],
                "constituency": person["constituency"],
                "county": person["county"],
                "position_title": primary_position.get("title", ""),
                "institution_name": primary_position.get(
                    "institution_name", ""
                ),
                "profile_url": person["profile_url"],
                "source_url": primary_source_row.get("source_url", ""),
                "entity_status": person["entity_status"]
            })


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print("Fetching persons and positions...")
    people = fetch_persons_with_positions(conn)

    print("Attaching citations...")
    attach_sources(conn, people)

    json_path = OUTPUT_DIR / "kenya_peps_export.json"
    csv_path = OUTPUT_DIR / "kenya_peps_export.csv"

    print(f"Writing {json_path}...")
    write_json(people, json_path)

    print(f"Writing {csv_path}...")
    write_csv(people, csv_path)

    print(f"\nDone. Exported {len(people)} active PEP records.")

    conn.close()


if __name__ == "__main__":
    main()
