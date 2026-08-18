# Lead Command Center

AI-powered lead ingestion and triage system with:
- FastAPI webhook ingestion
- OpenAI structured lead analysis
- SQLite persistence via SQLAlchemy
- Streamlit bilingual (English/Hebrew) dashboard with RTL-safe rendering

## Architecture

- `main.py`: API endpoints (`/webhook/lead`, `/leads`, workflow and analytics routes)
- `models.py`: SQLAlchemy models and Pydantic schemas
- `database.py`: async DB engine/session and initialization
- `ai_processor.py`: GPT-based lead analysis and retry logic
- `dashboard.py`: command center UI (metrics, funnel, saved views, lead actions)

## Quick Start

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Create environment file:
   - `copy .env.example .env` (Windows)
   - Fill `OPENAI_API_KEY`.
3. Start API:
   - `uvicorn main:app --reload --host 127.0.0.1 --port 8000`
4. Start dashboard:
   - `streamlit run dashboard.py`
5. Open Streamlit URL printed in terminal (usually `http://localhost:8501`).

## API Endpoints

- `POST /webhook/lead`
  - Accepts lead payload with `message` or `body`.
  - Optional idempotency key: `event_id`.
  - Optional auth headers:
    - `x-webhook-token` (when `WEBHOOK_AUTH_TOKEN` is set)
    - `x-webhook-signature` (HMAC SHA256 when `WEBHOOK_HMAC_SECRET` is set)
- `GET /leads`
  - Filters: `limit`, `offset`, `urgency`, `source`, `status`, `owner`
- `PATCH /leads/{lead_id}`
  - Updates lead `status` and `owner`
- `POST /leads/{lead_id}/activities`
  - Adds a note/activity to a lead
- `GET /leads/{lead_id}/activities`
  - Lists recent lead activities
- `GET /analytics/funnel`
  - Returns counts for `new`, `contacted`, `qualified`, `won`, `lost`

## Hebrew and RTL Notes

- AI prompt requests summary/reply in the same language as input.
- Dashboard includes a UI language switch (`English` / `עברית`).
- Hebrew rendering uses `direction: rtl`, `text-align: right`, and `unicode-bidi: plaintext`.
- Mixed-language content is displayed per-cell (not globally RTL) to keep English rows readable.

## Troubleshooting

- If dashboard cannot connect to API, verify `API_BASE_URL` and that `uvicorn` is running.
- If ingestion returns AI error, check `OPENAI_API_KEY`, model name, and timeout settings.
- If webhook returns 401, verify token/signature headers against `.env` values.
