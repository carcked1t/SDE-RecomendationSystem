from fastapi.testclient import TestClient
from app.main import app
from scripts.init_db import init as init_db

client = TestClient(app)


def test_search_category_case_insensitive():
    # Ensure DB is seeded for a deterministic test
    init_db()

    r1 = client.get("/products/search?category=Books&size=100")
    r2 = client.get("/products/search?category=books&size=100")
    r3 = client.get("/products/search?category=  bOoKs  &size=100")

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200

    ids1 = sorted([p["id"] for p in r1.json()])
    ids2 = sorted([p["id"] for p in r2.json()])
    ids3 = sorted([p["id"] for p in r3.json()])

    assert ids1 == ids2 == ids3
