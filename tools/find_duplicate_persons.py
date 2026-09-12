"""
Detects likely duplicate person records using normalized name
similarity. READ-ONLY — does not modify the database.

Run:
    python tools/find_duplicate_persons.py
"""

import re
import sqlite3
from difflib import SequenceMatcher
from pathlib import Path


DB_PATH = Path("database/compliance.db")

SIMILARITY_THRESHOLD = 0.72

HONORIFICS = [
    "rt. hon.", "rt hon", "hon.", "hon", "dr.", "dr", "prof.", "prof",
    "mr.", "mr", "mrs.", "mrs", "ms.", "ms", "amb.", "amb",
    "eng.", "eng", "col", "col.", "rtd", "(rtd)",
    "justice", "lady", "sir",
]

SUFFIXES = [
    "cbs", "egh", "mbs", "ogw", "ebs", "sc", "mp", "fcpa",
    "e.g.h", "e.g.h.", "c.g.h", "c.g.h.", "phd", "ph.d",
]


def normalize_name(raw_name: str) -> str:
    name = raw_name.lower()

    # Remove parenthetical content e.g. "(rtd)"
    name = re.sub(r"\([^)]*\)", " ", name)

    # Remove punctuation except commas (comma tells us about
    # "Last, First" ordering before we strip it)
    name = re.sub(r"[.\u2019']", " ", name)

    # Handle "Last, First Middle" -> "First Middle Last"
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        if len(parts) == 2 and parts[0] and parts[1]:
            name = f"{parts[1]} {parts[0]}"

    # Tokenize and strip honorifics / suffixes
    tokens = re.split(r"[\s,]+", name)
    tokens = [t for t in tokens if t]

    cleaned = []
    for t in tokens:
        t_clean = t.strip(".,")
        if t_clean in HONORIFICS or t_clean in SUFFIXES:
            continue
        if not t_clean:
            continue
        cleaned.append(t_clean)

    # Sort tokens so word order doesn't affect comparison
    # (helps "First Last" vs "Last First" residual cases)
    cleaned.sort()

    return " ".join(cleaned)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT person_id, full_name, primary_source FROM persons "
        "WHERE entity_status != 'MERGED'"
    )
    persons = cur.fetchall()

    print(f"Loaded {len(persons)} persons.\n")

    normalized = []
    for p in persons:
        normalized.append({
            "person_id": p["person_id"],
            "full_name": p["full_name"],
            "primary_source": p["primary_source"],
            "norm": normalize_name(p["full_name"]),
        })

    candidates = []

    for i in range(len(normalized)):
        for j in range(i + 1, len(normalized)):
            a = normalized[i]
            b = normalized[j]

            if not a["norm"] or not b["norm"]:
                continue

            # Cheap pre-filter: skip pairs with wildly different
            # lengths before running the more expensive ratio.
            if abs(len(a["norm"]) - len(b["norm"])) > 15:
                continue

            score = similarity(a["norm"], b["norm"])

            if score >= SIMILARITY_THRESHOLD:
                candidates.append((score, a, b))

    candidates.sort(key=lambda x: -x[0])

    print(f"Found {len(candidates)} candidate duplicate pair(s) "
          f"(threshold={SIMILARITY_THRESHOLD}):\n")

    for score, a, b in candidates:
        print(f"[{score:.3f}] "
              f"#{a['person_id']:>4} {a['full_name']!r:50} "
              f"({a['primary_source']})")
        print(f"        "
              f"#{b['person_id']:>4} {b['full_name']!r:50} "
              f"({b['primary_source']})")
        print()

    conn.close()


if __name__ == "__main__":
    main()
