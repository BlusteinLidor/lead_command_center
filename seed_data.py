"""Fictional clinic lead seed for the portfolio demo — no real PII."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Lead

# Theme: "Almond Family Clinic" / מרפאת שקד — fictional local clinic.
SEED_LEADS: List[Dict[str, Any]] = [
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name": "נועה כהן",
        "contact_email": None,
        "contact_phone": "+972-50-7001001",
        "message_body": (
            "שלום, אני מחפשת תור לרופא משפחה בהקדם. "
            "יש לי חום כבר שלושה ימים — אפשר להיום?"
        ),
        "score": 92,
        "summary": "פנייה דחופה לתור רופא משפחה באותו יום בשל חום מתמשך.",
        "urgency": "High",
        "detected_intent": "תור דחוף",
        "stage": "New",
        "hours_ago": 1,
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name": "Daniel Berger",
        "contact_email": "daniel.berger.demo@example.com",
        "contact_phone": "+972-52-7001002",
        "message_body": (
            "Looking for a pediatric checkup for my 4-year-old next week. "
            "Do you accept new patients at Almond Family Clinic?"
        ),
        "score": 78,
        "summary": "New-patient inquiry for a pediatric checkup within the next week.",
        "urgency": "Med",
        "detected_intent": "new patient / pediatrics",
        "stage": "Contacted",
        "hours_ago": 5,
    },
    {
        "source": "facebook",
        "channel": "lead_ad",
        "contact_name": "מיכל לוי",
        "contact_email": "michal.levi.demo@example.co.il",
        "contact_phone": "+972-54-7001003",
        "message_body": (
            "ראיתי מודעה על בדיקות דם מהירות. כמה זה עולה ומתי יש תורים?"
        ),
        "score": 71,
        "summary": "שאלה על מחיר ותורים לבדיקות דם בעקבות מודעת פייסבוק.",
        "urgency": "Med",
        "detected_intent": "תמחור / בדיקות",
        "stage": "New",
        "hours_ago": 8,
    },
    {
        "source": "phone",
        "channel": "callback_request",
        "contact_name": "Yossi Avraham",
        "contact_email": None,
        "contact_phone": "+972-50-7001004",
        "message_body": (
            "Please call me back about physiotherapy sessions after knee surgery. "
            "Insurance covers part of it."
        ),
        "score": 85,
        "summary": "Callback request for post-surgery physiotherapy; partial insurance coverage.",
        "urgency": "High",
        "detected_intent": "physiotherapy booking",
        "stage": "Qualified",
        "hours_ago": 12,
    },
    {
        "source": "email",
        "channel": "inbound",
        "contact_name": "שירה בן-דוד",
        "contact_email": "shira.bendavid.demo@example.org",
        "contact_phone": None,
        "message_body": (
            "אנחנו משפחה חדשה בשכונה. מחפשים רופא ילדים קבוע למרפאה. "
            "אפשר לקבל פרטים על שעות קבלה?"
        ),
        "score": 74,
        "summary": "משפחה חדשה מחפשת רופא ילדים קבוע ושעות קבלה במרפאה.",
        "urgency": "Med",
        "detected_intent": "רופא קבוע",
        "stage": "Contacted",
        "hours_ago": 20,
    },
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name": "Omar Hadad",
        "contact_email": "omar.hadad.demo@example.com",
        "contact_phone": "+972-58-7001005",
        "message_body": (
            "Need a same-week dermatology consult for a rash. "
            "Can you send available slots?"
        ),
        "score": 81,
        "summary": "Same-week dermatology consult request for a rash; wants available slots.",
        "urgency": "High",
        "detected_intent": "dermatology appointment",
        "stage": "New",
        "hours_ago": 3,
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name": "רונית פלד",
        "contact_email": "ronit.peled.demo@example.co.il",
        "contact_phone": "+972-52-7001006",
        "message_body": (
            "אשמח לקבל הצעת מחיר לחבילת בדיקות תקופתיות לעובדים בחברה קטנה (12 איש)."
        ),
        "score": 88,
        "summary": "בקשת הצעת מחיר לבדיקות תקופתיות ל-12 עובדים בחברה קטנה.",
        "urgency": "Med",
        "detected_intent": "הצעת מחיר ארגונית",
        "stage": "Qualified",
        "hours_ago": 28,
    },
    {
        "source": "email",
        "channel": "reply",
        "contact_name": "Tal Oran",
        "contact_email": "tal.oran.demo@example.co.il",
        "contact_phone": None,
        "message_body": (
            "Thanks for the vaccination reminder email. "
            "I already booked elsewhere — please cancel any pending slot."
        ),
        "score": 22,
        "summary": "Patient already booked elsewhere; asks to cancel any pending vaccination slot.",
        "urgency": "Low",
        "detected_intent": "cancellation",
        "stage": "Closed",
        "hours_ago": 36,
    },
    {
        "source": "instagram",
        "channel": "dm",
        "contact_name": "ליהי ברק",
        "contact_email": None,
        "contact_phone": "+972-54-7001007",
        "message_body": (
            "היי, ראיתי את הסטורי על ייעוץ תזונה. "
            "יש דיאטנית במרפאה? כמה עולה מפגש ראשון?"
        ),
        "score": 66,
        "summary": "שאלה על ייעוץ תזונה ומחיר מפגש ראשון בעקבות סטורי באינסטגרם.",
        "urgency": "Low",
        "detected_intent": "תזונה / תמחור",
        "stage": "New",
        "hours_ago": 48,
    },
    {
        "source": "phone",
        "channel": "front_desk",
        "contact_name": "Chris Vale",
        "contact_email": "chris.vale.demo@example.net",
        "contact_phone": "+972-50-7001008",
        "message_body": (
            "Wrong number — I was trying to reach a taxi. Sorry for the trouble."
        ),
        "score": 8,
        "summary": "Misdialed call; not a patient inquiry.",
        "urgency": "Low",
        "detected_intent": "wrong number",
        "stage": "Closed",
        "hours_ago": 52,
    },
]


def _lead_from_seed(item: Dict[str, Any]) -> Lead:
    hours_ago = int(item.get("hours_ago", 0))
    created = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    payload = {
        "source": item.get("source"),
        "channel": item.get("channel"),
        "name": item.get("contact_name"),
        "email": item.get("contact_email"),
        "phone": item.get("contact_phone"),
        "message": item["message_body"],
        "seed": True,
    }
    return Lead(
        created_at=created,
        raw_payload=payload,
        source=item.get("source"),
        channel=item.get("channel"),
        contact_name=item.get("contact_name"),
        contact_email=item.get("contact_email"),
        contact_phone=item.get("contact_phone"),
        message_body=item["message_body"],
        score=int(item["score"]),
        summary=item["summary"],
        urgency=item["urgency"],
        detected_intent=item["detected_intent"],
        stage=item.get("stage", "New"),
    )


async def ensure_seeded(session: AsyncSession) -> int:
    """Insert seed leads only when the leads table is empty. Returns rows inserted."""
    count = await session.scalar(select(func.count()).select_from(Lead))
    if count and count > 0:
        return 0
    for item in SEED_LEADS:
        session.add(_lead_from_seed(item))
    await session.commit()
    return len(SEED_LEADS)


async def reset_and_seed(session: AsyncSession) -> int:
    """Delete all leads and re-insert the fictional seed set. Returns seed count."""
    await session.execute(delete(Lead))
    await session.commit()
    for item in SEED_LEADS:
        session.add(_lead_from_seed(item))
    await session.commit()
    return len(SEED_LEADS)
