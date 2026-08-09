from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

LeadStage = Literal["New", "Contacted", "Qualified", "Closed"]
LEAD_STAGES: Tuple[str, ...] = ("New", "Contacted", "Qualified", "Closed")


class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    raw_payload: Mapped[Dict[str, Any]] = mapped_column(SQLiteJSON, nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    channel: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    contact_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    message_body: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(16), nullable=False)
    detected_intent: Mapped[str] = mapped_column(String(512), nullable=False)
    stage: Mapped[str] = mapped_column(String(32), nullable=False, default="New")


class LeadWebhookPayload(BaseModel):
    """Inbound webhook body; simulates WhatsApp, webforms, or email."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    message: Optional[str] = None
    body: Optional[str] = None
    source: Optional[str] = None
    channel: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @model_validator(mode="after")
    def require_message_text(self) -> "LeadWebhookPayload":
        text = (self.message or self.body or "").strip()
        if not text:
            raise ValueError("Either 'message' or 'body' must be a non-empty string.")
        return self

    def message_text(self) -> str:
        return (self.message or self.body or "").strip()

    def to_stored_payload(self) -> Dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)


class LeadAnalysis(BaseModel):
    score: int = Field(ge=1, le=100)
    summary: str = Field(max_length=500)
    urgency: Literal["Low", "Med", "High"]
    detected_intent: str = Field(max_length=256)


class LeadStageUpdate(BaseModel):
    stage: LeadStage


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    source: Optional[str]
    channel: Optional[str]
    contact_name: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    message_body: str
    score: int
    summary: str
    urgency: str
    detected_intent: str
    stage: str

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        """SQLite often strips tzinfo; treat naive values as UTC and emit `Z`."""
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)
        return value.isoformat().replace("+00:00", "Z")
