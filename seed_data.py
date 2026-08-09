"""Fictional clinic lead seed for the portfolio demo — no real PII."""

import random
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


# Rotating pool for live “incoming lead” demo (no OpenAI; portfolio recording).
INBOUND_DEMO_LEADS: List[Dict[str, Any]] = [
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name": "עדי מזרחי",
        "contact_email": None,
        "contact_phone": "+972-50-7002001",
        "message_body": (
            "שלום, יש לי חום גבוה ושיעול כבר יומיים. "
            "אפשר תור לרופא משפחה היום במרפאת שקד?"
        ),
        "score": 94,
        "summary": "פנייה דחופה לתור רופא משפחה באותו יום בשל חום ושיעול.",
        "urgency": "High",
        "detected_intent": "תור דחוף",
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name": "Emma Lang",
        "contact_email": "emma.lang.demo@example.com",
        "contact_phone": "+972-50-7003001",
        "message_body": (
            "Looking for a pediatric checkup for my 3-year-old at Almond Family Clinic. "
            "Do you accept new patients next week?"
        ),
        "score": 76,
        "summary": "New-patient pediatric checkup request for next week.",
        "urgency": "Med",
        "detected_intent": "New patient booking",
    },
    {
        "source": "facebook",
        "channel": "lead_ad",
        "contact_name": "אורי ונועה",
        "contact_email": None,
        "contact_phone": "+972-52-7002003",
        "message_body": (
            "עברנו לשכונה ומחפשים רופא ילדים קבוע במרפאה. "
            "יש מקום למשפחה עם שני ילדים?"
        ),
        "score": 81,
        "summary": "משפחה חדשה מחפשת רופא ילדים קבוע לשני ילדים.",
        "urgency": "Med",
        "detected_intent": "רישום משפחה",
    },
    {
        "source": "phone",
        "channel": "callback_request",
        "contact_name": "Mark Ezra",
        "contact_email": None,
        "contact_phone": "+972-52-7003002",
        "message_body": (
            "Please call me back about physiotherapy after knee surgery. "
            "My insurance covers part of the sessions."
        ),
        "score": 88,
        "summary": "Callback for post-surgery physio; insurance partially covers.",
        "urgency": "High",
        "detected_intent": "Physio callback",
    },
    {
        "source": "instagram",
        "channel": "dm",
        "contact_name": "נועה אלון",
        "contact_email": None,
        "contact_phone": "+972-58-7002004",
        "message_body": (
            "היי, ראיתי סטורי על ייעוץ תזונה. יש דיאטנית במרפאת שקד? מחיר מפגש ראשון?"
        ),
        "score": 62,
        "summary": "שאלה על ייעוץ תזונה ומחיר מפגש ראשון בעקבות אינסטגרם.",
        "urgency": "Low",
        "detected_intent": "תמחור ייעוץ",
    },
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name": "Sara Quinn",
        "contact_email": "sara.quinn.demo@example.com",
        "contact_phone": "+972-54-7003003",
        "message_body": (
            "Need a same-week dermatology consult for a rash on my arm. "
            "Can you send available slots?"
        ),
        "score": 90,
        "summary": "Same-week dermatology request for arm rash; wants available slots.",
        "urgency": "High",
        "detected_intent": "Dermatology booking",
    },
    {
        "source": "email",
        "channel": "inbound",
        "contact_name": "Jordan Pike",
        "contact_email": "jordan.pike.demo@example.com",
        "contact_phone": None,
        "message_body": (
            "We need a quote for annual employee checkups for a small company of 15 people. "
            "Are bulk packages available?"
        ),
        "score": 70,
        "summary": "Corporate quote request for 15 annual employee checkups.",
        "urgency": "Med",
        "detected_intent": "Corporate package",
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name": "יעל שרון",
        "contact_email": "yael.sharon.demo@example.co.il",
        "contact_phone": "+972-54-7002002",
        "message_body": (
            "ראיתי באתר שאתם עושים בדיקות דם בבוקר. כמה זה עולה בלי הפניה ומתי יש תורים?"
        ),
        "score": 58,
        "summary": "בירור מחיר וזמינות לבדיקות דם ללא הפניה.",
        "urgency": "Low",
        "detected_intent": "תמחור בדיקות",
    },
]


def _lead_from_seed(item: Dict[str, Any], *, live: bool = False) -> Lead:
    hours_ago = int(item.get("hours_ago", 0))
    created = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    payload = {
        "source": item.get("source"),
        "channel": item.get("channel"),
        "name": item.get("contact_name"),
        "email": item.get("contact_email"),
        "phone": item.get("contact_phone"),
        "message": item["message_body"],
        "seed": not live,
        "live_demo": live,
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


async def insert_live_incoming(session: AsyncSession) -> Lead:
    """Insert one randomized inbound demo lead (immediate New). No AI required."""
    base = dict(random.choice(INBOUND_DEMO_LEADS))
    base["stage"] = "New"
    base["hours_ago"] = 0
    # Light uniqueness so repeat arrivals feel fresh on camera.
    suffix = random.randint(10, 99)
    phone = base.get("contact_phone")
    if phone and phone[-2:].isdigit():
        base["contact_phone"] = phone[:-2] + f"{suffix:02d}"
    row = _lead_from_seed(base, live=True)
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row


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
