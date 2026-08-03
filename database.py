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


def _ensure_stage_column(sync_conn) -> None:
    """Add stage column to existing SQLite DBs created before the field existed."""
    inspector = inspect(sync_conn)
    if "leads" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("leads")}
    if "stage" not in cols:
        sync_conn.execute(
            text("ALTER TABLE leads ADD COLUMN stage VARCHAR(32) DEFAULT 'New'")
        )


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_ensure_stage_column)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
