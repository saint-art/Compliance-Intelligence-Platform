"""
REST API for the Compliance Intelligence Platform.

Exposes the Kenya PEP dataset for consumption by external systems
(e.g. the UN Sanctions Explorer portal). Read-only: this API never
writes to the database.

Run:
    python app.py

Endpoints:
    GET  /                          -> API index / route list
    GET  /api/health                -> health check
    GET  /api/stats                 -> summary statistics
    GET  /api/institutions          -> list of institutions with record counts
    GET  /api/persons               -> paginated, filterable list of active PEPs
    GET  /api/persons/<id>          -> single person, with positions + citations
    GET  /api/export/json           -> full dataset as JSON
    GET  /api/export/csv            -> full dataset as CSV
"""

import sqlite3
import csv
import io
from pathlib import Path
from flask import Flask, jsonify, request, g, Response

DB_PATH = Path("database/compliance.db")

app = Flask(__name__)


# ---------------------------------------------------------------
# DATABASE CONNECTION (request-scoped)
# ---------------------------------------------------------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------------------------------------------------------------
# CORS (manual -- no extra dependency required)
# ---------------------------------------------------------------

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------

def row_to_dict(row):
    return {k: row[k] for k in row.keys()}


def fetch_person_detail(conn, person_id):
    """
    Fetch one person with all their positions and citations
    attached as nested lists.
    """

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM persons WHERE person_id = ? "
        "AND entity_status != 'MERGED'",
        (person_id,)
    )
    person_row = cur.fetchone()

    if person_row is None:
        return None

    person = row_to_dict(person_row)

    cur.execute(
        """
        SELECT
            pos.title AS position_title,
            pos.category AS position_category,
            inst.institution_name,
            inst.category AS institution_category,
            pp.is_current,
            pp.start_date,
            pp.end_date
        FROM person_positions pp
        JOIN positions pos ON pos.position_id = pp.position_id
        JOIN institutions inst ON inst.institution_id = pp.institution_id
        WHERE pp.person_id = ?
        """,
        (person_id,)
    )
    person["positions"] = [row_to_dict(r) for r in cur.fetchall()]

    cur.execute(
        """
        SELECT source_name, source_url, source_type,
               trust_score, collected_at, last_verified
        FROM sources
        WHERE person_id = ?
        """,
        (person_id,)
    )
    person["sources"] = [row_to_dict(r) for r in cur.fetchall()]

    return person


# ---------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------

@app.route("/")
def index():
    return jsonify({
        "name": "Compliance Intelligence Platform API",
        "description": "Kenya PEP registry -- read-only REST API",
        "endpoints": {
            "GET /api/health": "Health check",
            "GET /api/stats": "Summary statistics",
            "GET /api/institutions": "List institutions with record counts",
            "GET /api/persons": (
                "Paginated, filterable list of active PEPs. "
                "Query params: page, per_page, institution, county, "
                "political_party, search"
            ),
            "GET /api/persons/<id>": (
                "Single person with positions and citations"
            ),
            "GET /api/export/json": "Full dataset as JSON",
            "GET /api/export/csv": "Full dataset as CSV",
        }
    })


@app.route("/api/health")
def health():
    try:
        conn = get_db()
        conn.execute("SELECT 1")
        return jsonify({"status": "ok"})
    except Exception as ex:
        return jsonify({"status": "error", "detail": str(ex)}), 500


@app.route("/api/stats")
def stats():

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) AS c FROM persons WHERE entity_status != 'MERGED'"
    )
    total_active = cur.fetchone()["c"]

    cur.execute(
        "SELECT COUNT(*) AS c FROM persons WHERE entity_status = 'MERGED'"
    )
    total_merged = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM sources")
    total_citations = cur.fetchone()["c"]

    cur.execute(
        "SELECT COUNT(DISTINCT institution_id) AS c FROM institutions"
    )
    total_institutions = cur.fetchone()["c"]

    cur.execute(
        """
        SELECT primary_source, COUNT(*) AS c
        FROM persons
        WHERE entity_status != 'MERGED'
        GROUP BY primary_source
        ORDER BY c DESC
        """
    )
    by_source = [row_to_dict(r) for r in cur.fetchall()]

    return jsonify({
        "total_active_persons": total_active,
        "total_merged_persons": total_merged,
        "total_citations": total_citations,
        "total_institutions": total_institutions,
        "by_source": by_source
    })


@app.route("/api/institutions")
def institutions():

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            inst.institution_id,
            inst.institution_name,
            inst.category,
            inst.country,
            COUNT(DISTINCT pp.person_id) AS person_count
        FROM institutions inst
        LEFT JOIN person_positions pp
            ON pp.institution_id = inst.institution_id
        LEFT JOIN persons p
            ON p.person_id = pp.person_id
            AND p.entity_status != 'MERGED'
        GROUP BY inst.institution_id
        ORDER BY person_count DESC
        """
    )

    return jsonify([row_to_dict(r) for r in cur.fetchall()])


@app.route("/api/persons")
def persons():

    conn = get_db()
    cur = conn.cursor()

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 50, type=int), 200)
    institution = request.args.get("institution")
    county = request.args.get("county")
    political_party = request.args.get("political_party")
    search = request.args.get("search")

    conditions = ["p.entity_status != 'MERGED'"]
    params = []

    if institution:
        conditions.append(
            "p.person_id IN ("
            "  SELECT pp.person_id FROM person_positions pp "
            "  JOIN institutions i ON i.institution_id = pp.institution_id "
            "  WHERE i.institution_name LIKE ?"
            ")"
        )
        params.append(f"%{institution}%")

    if county:
        conditions.append("p.county LIKE ?")
        params.append(f"%{county}%")

    if political_party:
        conditions.append("p.political_party LIKE ?")
        params.append(f"%{political_party}%")

    if search:
        conditions.append("p.full_name LIKE ?")
        params.append(f"%{search}%")

    where_clause = " AND ".join(conditions)

    cur.execute(
        f"SELECT COUNT(*) AS c FROM persons p WHERE {where_clause}",
        params
    )
    total = cur.fetchone()["c"]

    offset = (page - 1) * per_page

    cur.execute(
        f"""
        SELECT p.person_id, p.full_name, p.is_pep, p.is_sanctioned,
               p.risk_level, p.confidence_score, p.primary_source,
               p.political_party, p.constituency, p.county,
               p.profile_url, p.image_url
        FROM persons p
        WHERE {where_clause}
        ORDER BY p.person_id
        LIMIT ? OFFSET ?
        """,
        params + [per_page, offset]
    )

    results = [row_to_dict(r) for r in cur.fetchall()]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page,
        "results": results
    })


@app.route("/api/persons/<int:person_id>")
def person_detail(person_id):

    conn = get_db()
    person = fetch_person_detail(conn, person_id)

    if person is None:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(person)


@app.route("/api/export/json")
def export_json():

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT person_id FROM persons WHERE entity_status != 'MERGED' "
        "ORDER BY person_id"
    )
    ids = [r["person_id"] for r in cur.fetchall()]

    people = [fetch_person_detail(conn, pid) for pid in ids]

    return jsonify({
        "total_records": len(people),
        "persons": people
    })


@app.route("/api/export/csv")
def export_csv():

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            p.person_id, p.full_name, p.is_pep, p.is_sanctioned,
            p.risk_level, p.confidence_score, p.primary_source,
            p.political_party, p.constituency, p.county,
            p.profile_url, p.entity_status,
            pos.title AS position_title,
            inst.institution_name
        FROM persons p
        LEFT JOIN person_positions pp ON pp.person_id = p.person_id
        LEFT JOIN positions pos ON pos.position_id = pp.position_id
        LEFT JOIN institutions inst ON inst.institution_id = pp.institution_id
        WHERE p.entity_status != 'MERGED'
        ORDER BY p.person_id
        """
    )

    rows = cur.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "person_id", "full_name", "is_pep", "is_sanctioned",
        "risk_level", "confidence_score", "primary_source",
        "political_party", "constituency", "county",
        "profile_url", "entity_status", "position_title",
        "institution_name"
    ])

    for r in rows:
        writer.writerow([
            r["person_id"], r["full_name"], r["is_pep"],
            r["is_sanctioned"], r["risk_level"], r["confidence_score"],
            r["primary_source"], r["political_party"],
            r["constituency"], r["county"], r["profile_url"],
            r["entity_status"], r["position_title"],
            r["institution_name"]
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; filename=kenya_peps_export.csv"
            )
        }
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
