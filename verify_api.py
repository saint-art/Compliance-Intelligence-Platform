"""
Verifies every API endpoint works correctly using Flask's test
client -- no live server required.
"""

import json
from app import app

client = app.test_client()


def check(name, response, expect_status=200):
    status_ok = response.status_code == expect_status
    marker = "PASS" if status_ok else "FAIL"
    print(f"[{marker}] {name} -> HTTP {response.status_code}")
    return status_ok


all_ok = True

r = client.get("/")
all_ok &= check("GET /", r)

r = client.get("/api/health")
all_ok &= check("GET /api/health", r)
data = json.loads(r.data)
print(f"       status: {data.get('status')}")

r = client.get("/api/stats")
all_ok &= check("GET /api/stats", r)
data = json.loads(r.data)
print(f"       total_active_persons: {data.get('total_active_persons')}")
print(f"       total_citations: {data.get('total_citations')}")
print(f"       total_institutions: {data.get('total_institutions')}")
print(f"       by_source count: {len(data.get('by_source', []))}")

r = client.get("/api/institutions")
all_ok &= check("GET /api/institutions", r)
data = json.loads(r.data)
print(f"       institutions returned: {len(data)}")

r = client.get("/api/persons")
all_ok &= check("GET /api/persons", r)
data = json.loads(r.data)
print(f"       total: {data.get('total')}, page results: {len(data.get('results', []))}")

r = client.get("/api/persons?institution=Senate")
all_ok &= check("GET /api/persons?institution=Senate", r)
data = json.loads(r.data)
print(f"       Senate filter total: {data.get('total')}")

r = client.get("/api/persons?search=Ruto")
all_ok &= check("GET /api/persons?search=Ruto", r)
data = json.loads(r.data)
print(f"       search=Ruto results: {data.get('total')}")
for p in data.get("results", [])[:3]:
    print(f"         - {p['full_name']}")

r = client.get("/api/persons")
first_id = json.loads(r.data)["results"][0]["person_id"]
r = client.get(f"/api/persons/{first_id}")
all_ok &= check(f"GET /api/persons/{first_id}", r)
data = json.loads(r.data)
print(f"       name: {data.get('full_name')}")
print(f"       positions: {len(data.get('positions', []))}")
print(f"       sources: {len(data.get('sources', []))}")

r = client.get("/api/persons/999999")
all_ok &= check("GET /api/persons/999999 (should 404)", r, expect_status=404)

r = client.get("/api/export/json")
all_ok &= check("GET /api/export/json", r)
data = json.loads(r.data)
print(f"       total_records: {data.get('total_records')}")

r = client.get("/api/export/csv")
all_ok &= check("GET /api/export/csv", r)
print(f"       content-type: {r.content_type}")
print(f"       bytes: {len(r.data)}")

print()
print("=" * 50)
print("ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
print("=" * 50)
