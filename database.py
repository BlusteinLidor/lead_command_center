import os

from dotenv import load_dotenv
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./leads.db")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Columns added after the original schema; SQLite needs ALTER for existing DBs.
_OPTIONAL_LEAD_COLUMNS: tuple[tuple[str, str], ...] = (
    ("stage", "VARCHAR(32) DEFAULT 'New'"),
    ("contact_name_en", "VARCHAR(256)"),
    ("contact_name_he", "VARCHAR(256)"),
    ("message_body_en", "TEXT"),
    ("message_body_he", "TEXT"),
    ("summary_en", "TEXT"),
    ("summary_he", "TEXT"),
    ("detected_intent_en", "VARCHAR(512)"),
    ("detected_intent_he", "VARCHAR(512)"),
)


def _ensure_lead_columns(sync_conn) -> None:
    """Add newer lead columns to existing SQLite DBs created before those fields existed."""
    inspector = inspect(sync_conn)
    if "leads" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("leads")}
    for name, col_type in _OPTIONAL_LEAD_COLUMNS:
        if name not in cols:
            sync_conn.execute(text(f"ALTER TABLE leads ADD COLUMN {name} {col_type}"))


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_ensure_lead_columns)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
