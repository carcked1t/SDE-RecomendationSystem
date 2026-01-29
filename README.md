# Mini Amazon — Product Search & Recommendation System 🚀

**Short description**

A beginner-friendly, resume-worthy demo project implementing a product search and recommendation backend with a small demo frontend. Built with FastAPI, SQLAlchemy, and Pydantic (v2) — includes search filtering, simple recommendations, caching, and click/view tracking.

---

## 🔑 Key features (resume bullets)

- **FastAPI backend** with clean RESTful endpoints for product CRUD, search, analytics (views/clicks) and recommendations ✅
- **Search** supporting text queries and filters (category, price range, rating) with **case-insensitive** category matching ✅
- **Simple recommendation logic** (same category + price proximity) and a **popularity ranking** using rating × log(views) + clicks ✅
- **In-memory TTL cache** for search/popular responses to improve demo performance ✅
- **Frontend demo** (vanilla JS + static HTML) that calls the backend, hosted under `/demo` for convenience ✅
- **Pydantic v2**, SQLAlchemy ORM, migration-friendly structure — designed as a teaching/example project ✅
- **Unit test** demonstrating case-insensitive search behavior + simple smoke tests ✅

---

## 🏗️ Tech stack & design notes

- **Python 3.10+**, **FastAPI**, **Uvicorn**, **SQLAlchemy**, **Pydantic v2**
- **SQLite** for easy local demo (recommend switching to **Postgres** for production)
- Simple, deterministic scoring for popularity and related items (easy to explain in interviews)
- Cache keys are normalized (case + whitespace) to ensure consistent behavior

---

## ▶️ Quick run (local)

1. Create and activate a virtualenv:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Seed the database:

```bash
python scripts/init_db.py
```

4. Run the app:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

5. Open the demo: http://127.0.0.1:8000/demo or visit the OpenAPI docs at `/docs`.

---

## ✅ Tests

Run the unit tests:

```bash
python -m pytest -q
```

The repo includes a targeted test that ensures category searches are case-insensitive.

---

## ⚙️ API summary (important endpoints)

- `POST /products/add` — Add a product
- `GET /products/search` — Search with `q`, `category`, `min_price`, `max_price`, `min_rating`, `sort_by`, `page`, `size`
- `GET /products/{id}` — Get product
- `GET /products/{id}/view` — Increment view counter (affects popularity)
- `GET /products/{id}/click` — Increment click counter
- `GET /recommend/{product_id}` — Related products (same category + price proximity)
- `GET /recommend/popular` — Popular products

> All search/category matching is case-insensitive and cache keys are normalized.

---

## 📦 Deployment notes (short)

- Use **Docker** + managed Postgres for production.
- Quick providers: **Render**, **Railway**, **Fly**, **Cloud Run**; static frontend can go to **Vercel** if split.
- The repo contains a `Dockerfile` and sample CI workflow (see `.github/workflows/`).

---

## 🙋 Why this is interview/resume-friendly

- Small but complete full-stack demo showing API design, DB interactions, caching, and a tiny frontend.
- Contains deliberate trade-offs and simple algorithms you can confidently explain in interviews.
- Clean, modular code — easy to extend (swap DB, improve recommender, add auth).

---

## ✨ Contributing / Next steps

- Add Postgres support & example `DATABASE_URL` env config
- Add more tests (performance, recommendations, security)
- Add CI/CD workflow to push to GHCR or auto-deploy to Render

---

## License & contact

MIT — Feel free to reuse. Open an issue or PR if you want changes.

Happy building! 🔧✨
