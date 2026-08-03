import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List

from typing_extensions import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_processor import analyze_lead
from database import AsyncSessionLocal, get_db, init_db
from models import Lead, LeadAnalysis, LeadOut, LeadStageUpdate, LeadWebhookPayload
from seed_data import ensure_seeded, reset_and_seed

load_dotenv()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    async with AsyncSessionLocal() as session:
        await ensure_seeded(session)
    yield


app = FastAPI(title="Lead Command Center API", lifespan=lifespan)

_cors_extra = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        *_cors_extra,
    ],
    allow_origin_regex=r"https://.*\.streamlit\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DbSession = Annotated[AsyncSession, Depends(get_db)]


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/webhook/lead", response_model=LeadOut, status_code=status.HTTP_201_CREATED)
async def webhook_lead(payload: LeadWebhookPayload, db: DbSession) -> Lead:
    message = payload.message_text()
    extras = []
    if payload.name:
        extras.append(f"Name: {payload.name}")
    if payload.email:
        extras.append(f"Email: {payload.email}")
    if payload.phone:
        extras.append(f"Phone: {payload.phone}")
    if payload.source:
        extras.append(f"Source: {payload.source}")
    if payload.channel:
        extras.append(f"Channel: {payload.channel}")
    context = "\n".join(extras) if extras else None

    try:
        analysis: LeadAnalysis = await analyze_lead(message, context=context)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI processing failed: {e!s}",
        ) from e

    row = Lead(
        raw_payload=payload.to_stored_payload(),
        source=payload.source,
        channel=payload.channel,
        contact_name=payload.name,
        contact_email=payload.email,
        contact_phone=payload.phone,
        message_body=message,
        score=analysis.score,
        summary=analysis.summary,
        urgency=analysis.urgency,
        detected_intent=analysis.detected_intent,
        stage="New",
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


@app.get("/leads", response_model=List[LeadOut])
async def list_leads(db: DbSession, limit: int = 500) -> List[Lead]:
    if limit < 1 or limit > 2000:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 2000")
    result = await db.execute(select(Lead).order_by(Lead.created_at.desc()).limit(limit))
    return list(result.scalars().all())


@app.patch("/leads/{lead_id}/stage", response_model=LeadOut)
async def update_lead_stage(
    lead_id: int,
    body: LeadStageUpdate,
    db: DbSession,
) -> Lead:
    row = await db.get(Lead, lead_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    row.stage = body.stage
    await db.commit()
    await db.refresh(row)
    return row


@app.post("/demo/reset", response_model=dict)
async def demo_reset(db: DbSession) -> dict:
    """Wipe leads and restore fictional portfolio seed data."""
    count = await reset_and_seed(db)
    return {"ok": True, "seeded": count}
