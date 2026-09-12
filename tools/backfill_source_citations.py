"""
One-time backfill: creates citation rows in `sources` for every
person who predates the SourceRepository fix, using data already
present in the database (person_positions + source_documents).

No network requests -- entirely reconstructed from existing rows.

Skips:
  - Persons who already have at least one citation (avoids
    duplicating the 47 Governors just refreshed).
  - Tombstoned (MERGED) persons, since their person_positions
    rows were already removed during merge and they route
    through their canonical record instead.

Run:
    python tools/backfill_source_citations.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("database/compliance.db")


def main():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            pp.person_id,
            p.primary_source,
            p.confidence_score,
            sd.source_url,
            pp.created_at
        FROM person_positions pp
        JOIN persons p
            ON p.person_id = pp.person_id
        JOIN source_documents sd
            ON sd.document_id = pp.source_document_id
        WHERE pp.person_id NOT IN (
            SELECT DISTINCT person_id FROM sources
        )
        AND p.entity_status != 'MERGED'
        """
    )

    rows = cur.fetchall()

    print(f"Found {len(rows)} person_position row(s) needing backfill.")

    now = datetime.utcnow().isoformat()

    inserted = 0

    for row in rows:

        cur.execute(
            """
            INSERT INTO sources (
                person_id,
                source_name,
                source_url,
                source_type,
                trust_score,
                collected_at,
                last_verified
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["person_id"],
                row["primary_source"] or "",
                row["source_url"] or "",
                "HTML",
                row["confidence_score"],
                row["created_at"] or now,
                now
            )
        )

        inserted += 1

    conn.commit()

    print(f"Inserted {inserted} citation row(s).")

    cur.execute("SELECT COUNT(*) AS c FROM sources")
    total = cur.fetchone()["c"]

    print(f"Total citations in sources table: {total}")

    conn.close()


if __name__ == "__main__":
    main()
