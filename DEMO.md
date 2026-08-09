# Lead Command Center — portfolio demo

Public ops board demo: inbound clinic leads, AI score/summary, triage by stage.
**Primary UI:** React SPA. **API:** FastAPI + SQLite (+ optional OpenAI).

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then edit secrets
```

### Option A — one process (API + production UI)

```bash
cd frontend
npm install
npm run build
cd ..
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 — seeded clinic leads appear immediately.

### Option B — frontend dev server (hot reload)

```bash
# terminal 1
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# terminal 2
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — Vite proxies `/api/*` to the API.

### Demo happy path (&lt;60s)

1. Read brand + “Demo · sample data” chip.
2. Spot **High urgency** KPI and open a hot lead card.
3. In the drawer, change **stage** (e.g. New → Contacted / Qualified).
4. Confirm the Kanban column and KPIs update.
5. Optional: **Demo tools** → Reset demo data.
6. Optional: EN/HE language toggle (full RTL in Hebrew).
7. Optional: Demo tools → Simulate inbound lead (needs `OPENAI_API_KEY`).

## Environment / secrets

| Variable | Required | Notes |
|----------|----------|--------|
| `DATABASE_URL` | No | Default `sqlite+aiosqlite:///./leads.db` |
| `OPENAI_API_KEY` | Only for webhook simulator | Board + triage work without it |
| `CORS_ORIGINS` | No | Extra comma-separated origins (Vite `5173` is allowed by default) |
| `VITE_API_BASE` | No | Frontend only; default `/api` in dev, empty in production build |

## Reset data

- **UI:** Demo tools → Reset demo data (`POST /demo/reset`).
- Seed theme: fictional **Almond Family Clinic** / מרפאת שקד — no real PII.

## Deploy (public URL)

Streamlit Cloud cannot host this React UI. Use a single Docker service that serves FastAPI + the built SPA.

### Render (free tier, recommended)

1. **Commit and push** this repo to GitHub (`BlusteinLidor/lead_command_center`).
2. Open [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect the GitHub repo. Render reads [`render.yaml`](render.yaml) and creates `lead-command-center`.
4. Optional: set secret **`OPENAI_API_KEY`** for the lead simulator (board works without it).
5. Deploy → open `https://lead-command-center.onrender.com` (or your service URL).

**Manual alternative:** New → Web Service → Docker, root directory `.`, health check `/health`. Free instances sleep after idle; first load can take ~30–60s.

### Railway / Fly / any Docker host

```bash
docker build -t lead-command-center .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... lead-command-center
```

Or build without Docker:

```bash
cd frontend && npm ci && npm run build && cd ..
uvicorn main:app --host 0.0.0.0 --port 8000
```

SQLite on free hosts is ephemeral (re-seeds on cold start). That is fine for a portfolio demo.

Legacy Streamlit UI still exists as `dashboard.py` for reference; the product surface is the React app.

## API

- `GET /health`
- `GET /leads`
- `PATCH /leads/{id}/stage` — body `{"stage":"New"|"Contacted"|"Qualified"|"Closed"}`
- `POST /webhook/lead` — AI ingest (needs OpenAI)
- `POST /demo/reset` — wipe + re-seed

## Portfolio handoff

```text
id: lead-command-center
demoUrl: PENDING — deploy on Render via render.yaml (see Deploy above). Service name: lead-command-center
title_en: Lead Command Center
title_he: מרכז פיקוד לידים
problem_en: Leads arrive scattered across WhatsApp, forms, and email — follow-ups get missed in spreadsheets.
problem_he: לידים מגיעים מפוזרים בוואטסאפ, טפסים ומייל — מעקב נופל בין גיליונות.
solution_en: One ops board that ingests leads, scores and summarizes with AI, and lets you triage by stage.
solution_he: לוח תפעול אחד שקולט לידים, מדרג ומסכם עם AI, ומאפשר לנהל שלב בצינור המכירות.
result_en: Single source of truth — hot leads are visible immediately and staged in under a minute.
result_he: מקור אמת אחד — לידים חמים נראים מיד ועוברים שלב בפחות מדקה.
tech: FastAPI, React, TypeScript, Vite, Tailwind CSS, SQLite, OpenAI
videoUrl:
poster:
```
