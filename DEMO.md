# Lead Command Center — portfolio demo

Public Streamlit demo of an internal ops board: inbound leads, AI score/summary, triage by stage.

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then edit secrets
```

**Option A — single process (matches Streamlit Cloud):**

```bash
# DEMO_EMBED_API defaults on for localhost API_BASE_URL
streamlit run dashboard.py
```

**Option B — two processes:**

```bash
# terminal 1
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# terminal 2
set DEMO_EMBED_API=0
streamlit run dashboard.py
```

Open http://localhost:8501 — seeded clinic leads should appear immediately.

### Demo happy path (&lt;60s)

1. Read the portfolio banner (sample data only).
2. Under **Triage a lead**, pick a lead and change **stage** → **Update stage**.
3. Confirm the board and stage metrics update.
4. Optional: **Reset demo data** in the sidebar to restore the seed set.

### Simulate lead (optional)

Sidebar **Send test JSON to webhook** calls OpenAI. Requires `OPENAI_API_KEY`. The main board does **not** need OpenAI.

## Environment / secrets

| Variable | Required | Notes |
|----------|----------|--------|
| `DATABASE_URL` | No | Default `sqlite+aiosqlite:///./leads.db` |
| `API_BASE_URL` | No | Default `http://127.0.0.1:8000` |
| `DEMO_EMBED_API` | No | `1`/`0` — embed FastAPI inside Streamlit. Auto on Streamlit Cloud / localhost |
| `DEMO_API_PORT` | No | Default `8000` |
| `OPENAI_API_KEY` | Only for webhook simulator | Not needed to view/triage seed leads |
| `CORS_ORIGINS` | No | Extra comma-separated origins for the API |

Streamlit Community Cloud: set the same keys under **App settings → Secrets** (TOML), e.g.:

```toml
OPENAI_API_KEY = "sk-..."
DATABASE_URL = "sqlite+aiosqlite:///./leads.db"
API_BASE_URL = "http://127.0.0.1:8000"
DEMO_EMBED_API = "1"
```

## Reset data

- **UI:** sidebar → **Reset demo data** (`POST /demo/reset`).
- **Cloud reboot:** ephemeral disk clears; next start re-seeds if the DB is empty.
- Seed theme: fictional **Almond Family Clinic** / מרפאת שקד — no real PII.

## Deploy (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. https://share.streamlit.io → **New app** → select repo, branch, main file `dashboard.py`.
3. Add secrets (above). `OPENAI_API_KEY` optional.
4. Deploy and copy the `https://….streamlit.app` URL into the handoff block below.

## API (embedded or standalone)

- `GET /health`
- `GET /leads`
- `PATCH /leads/{id}/stage` — body `{"stage":"New"|"Contacted"|"Qualified"|"Closed"}`
- `POST /webhook/lead` — AI ingest (needs OpenAI)
- `POST /demo/reset` — wipe + re-seed

## Portfolio handoff

```text
id: lead-command-center
demoUrl: (fill after deploy)
title_en: Lead Command Center
title_he: מרכז פיקוד לידים
problem_en: Leads arrive scattered across WhatsApp, forms, and email — follow-ups get missed in spreadsheets.
problem_he: לידים מגיעים מפוזרים בוואטסאפ, טפסים ומייל — מעקב נופל בין גיליונות.
solution_en: One ops board that ingests leads, scores and summarizes with AI, and lets you triage by stage.
solution_he: לוח תפעול אחד שקולט לידים, מדרג ומסכם עם AI, ומאפשר לנהל שלב בצינור המכירות.
result_en: Single source of truth — hot leads are visible immediately and staged in under a minute.
result_he: מקור אמת אחד — לידים חמים נראים מיד ועוברים שלב בפחות מדקה.
tech: FastAPI, Streamlit, SQLite, OpenAI
videoUrl:
poster:
```
