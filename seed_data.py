"""Fictional clinic lead seed for the portfolio demo — no real PII.

Each lead stores English + Hebrew text so the UI language toggle can switch all
lead content without re-fetching or re-analyzing.
"""

import random
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Lead

# Theme: "Almond Family Clinic" / מרפאת שקד — fictional local clinic.
SEED_LEADS: List[Dict[str, Any]] = [
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name_en": "Noa Cohen",
        "contact_name_he": "נועה כהן",
        "contact_email": None,
        "contact_phone": "+972-50-7001001",
        "message_body_en": (
            "Hi, I'm looking for a family doctor appointment as soon as possible. "
            "I've had a fever for three days — can it be today?"
        ),
        "message_body_he": (
            "שלום, אני מחפשת תור לרופא משפחה בהקדם. "
            "יש לי חום כבר שלושה ימים — אפשר להיום?"
        ),
        "score": 92,
        "summary_en": "Urgent same-day family-doctor request due to ongoing fever.",
        "summary_he": "פנייה דחופה לתור רופא משפחה באותו יום בשל חום מתמשך.",
        "urgency": "High",
        "detected_intent_en": "Urgent appointment",
        "detected_intent_he": "תור דחוף",
        "stage": "New",
        "hours_ago": 1,
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name_en": "Daniel Berger",
        "contact_name_he": "דניאל ברגר",
        "contact_email": "daniel.berger.demo@example.com",
        "contact_phone": "+972-52-7001002",
        "message_body_en": (
            "Looking for a pediatric checkup for my 4-year-old next week. "
            "Do you accept new patients at Almond Family Clinic?"
        ),
        "message_body_he": (
            "מחפש בדיקת ילדים לבתי בת ה-4 לשבוע הבא. "
            "האם אתם מקבלים מטופלים חדשים במרפאת שקד?"
        ),
        "score": 78,
        "summary_en": "New-patient inquiry for a pediatric checkup within the next week.",
        "summary_he": "פניית מטופל חדש לבדיקת ילדים בטווח השבוע הקרוב.",
        "urgency": "Med",
        "detected_intent_en": "New patient / pediatrics",
        "detected_intent_he": "מטופל חדש / ילדים",
        "stage": "Contacted",
        "hours_ago": 5,
    },
    {
        "source": "facebook",
        "channel": "lead_ad",
        "contact_name_en": "Michal Levi",
        "contact_name_he": "מיכל לוי",
        "contact_email": "michal.levi.demo@example.co.il",
        "contact_phone": "+972-54-7001003",
        "message_body_en": (
            "I saw an ad about fast blood tests. How much does it cost and when are appointments available?"
        ),
        "message_body_he": (
            "ראיתי מודעה על בדיקות דם מהירות. כמה זה עולה ומתי יש תורים?"
        ),
        "score": 71,
        "summary_en": "Facebook-ad inquiry about blood-test pricing and appointment slots.",
        "summary_he": "שאלה על מחיר ותורים לבדיקות דם בעקבות מודעת פייסבוק.",
        "urgency": "Med",
        "detected_intent_en": "Pricing / labs",
        "detected_intent_he": "תמחור / בדיקות",
        "stage": "New",
        "hours_ago": 8,
    },
    {
        "source": "phone",
        "channel": "callback_request",
        "contact_name_en": "Yossi Avraham",
        "contact_name_he": "יוסי אברהם",
        "contact_email": None,
        "contact_phone": "+972-50-7001004",
        "message_body_en": (
            "Please call me back about physiotherapy sessions after knee surgery. "
            "Insurance covers part of it."
        ),
        "message_body_he": (
            "אשמח שיחזרו אליי לגבי טיפולי פיזיותרפיה אחרי ניתוח ברך. "
            "הביטוח מכסה חלק מהעלות."
        ),
        "score": 85,
        "summary_en": "Callback request for post-surgery physiotherapy; partial insurance coverage.",
        "summary_he": "בקשת חזרה טלפונית לפיזיותרפיה אחרי ניתוח; כיסוי ביטוחי חלקי.",
        "urgency": "High",
        "detected_intent_en": "Physiotherapy booking",
        "detected_intent_he": "הזמנת פיזיותרפיה",
        "stage": "Qualified",
        "hours_ago": 12,
    },
    {
        "source": "email",
        "channel": "inbound",
        "contact_name_en": "Shira Ben-David",
        "contact_name_he": "שירה בן-דוד",
        "contact_email": "shira.bendavid.demo@example.org",
        "contact_phone": None,
        "message_body_en": (
            "We're a new family in the neighborhood looking for a regular pediatrician. "
            "Can we get clinic hours?"
        ),
        "message_body_he": (
            "אנחנו משפחה חדשה בשכונה. מחפשים רופא ילדים קבוע למרפאה. "
            "אפשר לקבל פרטים על שעות קבלה?"
        ),
        "score": 74,
        "summary_en": "New family seeking a regular pediatrician and clinic hours.",
        "summary_he": "משפחה חדשה מחפשת רופא ילדים קבוע ושעות קבלה במרפאה.",
        "urgency": "Med",
        "detected_intent_en": "Regular doctor",
        "detected_intent_he": "רופא קבוע",
        "stage": "Contacted",
        "hours_ago": 20,
    },
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name_en": "Omar Hadad",
        "contact_name_he": "עומר חדד",
        "contact_email": "omar.hadad.demo@example.com",
        "contact_phone": "+972-58-7001005",
        "message_body_en": (
            "Need a same-week dermatology consult for a rash. "
            "Can you send available slots?"
        ),
        "message_body_he": (
            "צריך ייעוץ עור השבוע בגלל פריחה. "
            "אפשר לקבל מועדים פנויים?"
        ),
        "score": 81,
        "summary_en": "Same-week dermatology consult request for a rash; wants available slots.",
        "summary_he": "בקשה לייעוץ עור באותו שבוע בגלל פריחה; מבקש מועדים.",
        "urgency": "High",
        "detected_intent_en": "Dermatology appointment",
        "detected_intent_he": "תור עור",
        "stage": "New",
        "hours_ago": 3,
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name_en": "Ronit Peled",
        "contact_name_he": "רונית פלד",
        "contact_email": "ronit.peled.demo@example.co.il",
        "contact_phone": "+972-52-7001006",
        "message_body_en": (
            "I'd like a quote for periodic employee checkups for a small company (12 people)."
        ),
        "message_body_he": (
            "אשמח לקבל הצעת מחיר לחבילת בדיקות תקופתיות לעובדים בחברה קטנה (12 איש)."
        ),
        "score": 88,
        "summary_en": "Corporate quote request for periodic checkups for 12 employees.",
        "summary_he": "בקשת הצעת מחיר לבדיקות תקופתיות ל-12 עובדים בחברה קטנה.",
        "urgency": "Med",
        "detected_intent_en": "Corporate quote",
        "detected_intent_he": "הצעת מחיר ארגונית",
        "stage": "Qualified",
        "hours_ago": 28,
    },
    {
        "source": "email",
        "channel": "reply",
        "contact_name_en": "Tal Oran",
        "contact_name_he": "טל אורן",
        "contact_email": "tal.oran.demo@example.co.il",
        "contact_phone": None,
        "message_body_en": (
            "Thanks for the vaccination reminder email. "
            "I already booked elsewhere — please cancel any pending slot."
        ),
        "message_body_he": (
            "תודה על תזכורת החיסון במייל. "
            "כבר הזמנתי במקום אחר — בבקשה לבטל כל תור פתוח."
        ),
        "score": 22,
        "summary_en": "Patient already booked elsewhere; asks to cancel any pending vaccination slot.",
        "summary_he": "המטופל כבר הזמין במקום אחר; מבקש לבטל תור חיסון פתוח.",
        "urgency": "Low",
        "detected_intent_en": "Cancellation",
        "detected_intent_he": "ביטול",
        "stage": "Closed",
        "hours_ago": 36,
    },
    {
        "source": "instagram",
        "channel": "dm",
        "contact_name_en": "Lihi Barak",
        "contact_name_he": "ליהי ברק",
        "contact_email": None,
        "contact_phone": "+972-54-7001007",
        "message_body_en": (
            "Hi, I saw the story about nutrition counseling. "
            "Do you have a dietitian at the clinic? What's the price for a first session?"
        ),
        "message_body_he": (
            "היי, ראיתי את הסטורי על ייעוץ תזונה. "
            "יש דיאטנית במרפאה? כמה עולה מפגש ראשון?"
        ),
        "score": 66,
        "summary_en": "Instagram story inquiry about nutrition counseling and first-session price.",
        "summary_he": "שאלה על ייעוץ תזונה ומחיר מפגש ראשון בעקבות סטורי באינסטגרם.",
        "urgency": "Low",
        "detected_intent_en": "Nutrition / pricing",
        "detected_intent_he": "תזונה / תמחור",
        "stage": "New",
        "hours_ago": 48,
    },
    {
        "source": "phone",
        "channel": "front_desk",
        "contact_name_en": "Chris Vale",
        "contact_name_he": "כריס וייל",
        "contact_email": "chris.vale.demo@example.net",
        "contact_phone": "+972-50-7001008",
        "message_body_en": (
            "Wrong number — I was trying to reach a taxi. Sorry for the trouble."
        ),
        "message_body_he": (
            "מספר שגוי — ניסיתי להשיג מונית. סליחה על ההפרעה."
        ),
        "score": 8,
        "summary_en": "Misdialed call; not a patient inquiry.",
        "summary_he": "חיוג בטעות; לא פניית מטופל.",
        "urgency": "Low",
        "detected_intent_en": "Wrong number",
        "detected_intent_he": "מספר שגוי",
        "stage": "Closed",
        "hours_ago": 52,
    },
]


# Rotating pool for live “incoming lead” demo (no OpenAI; portfolio recording).
INBOUND_DEMO_LEADS: List[Dict[str, Any]] = [
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name_en": "Adi Mizrahi",
        "contact_name_he": "עדי מזרחי",
        "contact_email": None,
        "contact_phone": "+972-50-7002001",
        "message_body_en": (
            "Hi, I've had a high fever and cough for two days. "
            "Can I get a family-doctor appointment today at Almond Family Clinic?"
        ),
        "message_body_he": (
            "שלום, יש לי חום גבוה ושיעול כבר יומיים. "
            "אפשר תור לרופא משפחה היום במרפאת שקד?"
        ),
        "score": 94,
        "summary_en": "Urgent same-day family-doctor request due to fever and cough.",
        "summary_he": "פנייה דחופה לתור רופא משפחה באותו יום בשל חום ושיעול.",
        "urgency": "High",
        "detected_intent_en": "Urgent appointment",
        "detected_intent_he": "תור דחוף",
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name_en": "Emma Lang",
        "contact_name_he": "אמה לאנג",
        "contact_email": "emma.lang.demo@example.com",
        "contact_phone": "+972-50-7003001",
        "message_body_en": (
            "Looking for a pediatric checkup for my 3-year-old at Almond Family Clinic. "
            "Do you accept new patients next week?"
        ),
        "message_body_he": (
            "מחפשת בדיקת ילדים לבן 3 במרפאת שקד. "
            "האם אתם מקבלים מטופלים חדשים בשבוע הבא?"
        ),
        "score": 76,
        "summary_en": "New-patient pediatric checkup request for next week.",
        "summary_he": "בקשת מטופל חדש לבדיקת ילדים לשבוע הבא.",
        "urgency": "Med",
        "detected_intent_en": "New patient booking",
        "detected_intent_he": "הזמנת מטופל חדש",
    },
    {
        "source": "facebook",
        "channel": "lead_ad",
        "contact_name_en": "Uri and Noa",
        "contact_name_he": "אורי ונועה",
        "contact_email": None,
        "contact_phone": "+972-52-7002003",
        "message_body_en": (
            "We just moved to the neighborhood and need a regular pediatrician. "
            "Is there room for a family with two kids?"
        ),
        "message_body_he": (
            "עברנו לשכונה ומחפשים רופא ילדים קבוע במרפאה. "
            "יש מקום למשפחה עם שני ילדים?"
        ),
        "score": 81,
        "summary_en": "New family seeking a regular pediatrician for two children.",
        "summary_he": "משפחה חדשה מחפשת רופא ילדים קבוע לשני ילדים.",
        "urgency": "Med",
        "detected_intent_en": "Family registration",
        "detected_intent_he": "רישום משפחה",
    },
    {
        "source": "phone",
        "channel": "callback_request",
        "contact_name_en": "Mark Ezra",
        "contact_name_he": "מארק עזרא",
        "contact_email": None,
        "contact_phone": "+972-52-7003002",
        "message_body_en": (
            "Please call me back about physiotherapy after knee surgery. "
            "My insurance covers part of the sessions."
        ),
        "message_body_he": (
            "אנא חזרו אליי לגבי פיזיותרפיה אחרי ניתוח ברך. "
            "הביטוח שלי מכסה חלק מהטיפולים."
        ),
        "score": 88,
        "summary_en": "Callback for post-surgery physio; insurance partially covers.",
        "summary_he": "בקשת חזרה לפיזיותרפיה אחרי ניתוח; כיסוי ביטוחי חלקי.",
        "urgency": "High",
        "detected_intent_en": "Physio callback",
        "detected_intent_he": "חזרה לפיזיותרפיה",
    },
    {
        "source": "instagram",
        "channel": "dm",
        "contact_name_en": "Noa Alon",
        "contact_name_he": "נועה אלון",
        "contact_email": None,
        "contact_phone": "+972-58-7002004",
        "message_body_en": (
            "Hi, I saw a story about nutrition counseling. Is there a dietitian at Almond Family Clinic? First-session price?"
        ),
        "message_body_he": (
            "היי, ראיתי סטורי על ייעוץ תזונה. יש דיאטנית במרפאת שקד? מחיר מפגש ראשון?"
        ),
        "score": 62,
        "summary_en": "Nutrition counseling pricing question after Instagram.",
        "summary_he": "שאלה על ייעוץ תזונה ומחיר מפגש ראשון בעקבות אינסטגרם.",
        "urgency": "Low",
        "detected_intent_en": "Counseling pricing",
        "detected_intent_he": "תמחור ייעוץ",
    },
    {
        "source": "whatsapp",
        "channel": "chat",
        "contact_name_en": "Sara Quinn",
        "contact_name_he": "שרה קווין",
        "contact_email": "sara.quinn.demo@example.com",
        "contact_phone": "+972-54-7003003",
        "message_body_en": (
            "Need a same-week dermatology consult for a rash on my arm. "
            "Can you send available slots?"
        ),
        "message_body_he": (
            "צריכה ייעוץ עור השבוע בגלל פריחה ביד. "
            "אפשר לקבל מועדים פנויים?"
        ),
        "score": 90,
        "summary_en": "Same-week dermatology request for arm rash; wants available slots.",
        "summary_he": "בקשת ייעוץ עור באותו שבוע לפריחה ביד; מבקשת מועדים.",
        "urgency": "High",
        "detected_intent_en": "Dermatology booking",
        "detected_intent_he": "הזמנת עור",
    },
    {
        "source": "email",
        "channel": "inbound",
        "contact_name_en": "Jordan Pike",
        "contact_name_he": "ג'ורדן פייק",
        "contact_email": "jordan.pike.demo@example.com",
        "contact_phone": None,
        "message_body_en": (
            "We need a quote for annual employee checkups for a small company of 15 people. "
            "Are bulk packages available?"
        ),
        "message_body_he": (
            "אנחנו צריכים הצעת מחיר לבדיקות שנתיות לעובדים בחברה של 15 איש. "
            "יש חבילות בכמות?"
        ),
        "score": 70,
        "summary_en": "Corporate quote request for 15 annual employee checkups.",
        "summary_he": "בקשת הצעת מחיר לבדיקות שנתיות ל-15 עובדים.",
        "urgency": "Med",
        "detected_intent_en": "Corporate package",
        "detected_intent_he": "חבילה ארגונית",
    },
    {
        "source": "webform",
        "channel": "contact",
        "contact_name_en": "Yael Sharon",
        "contact_name_he": "יעל שרון",
        "contact_email": "yael.sharon.demo@example.co.il",
        "contact_phone": "+972-54-7002002",
        "message_body_en": (
            "I saw on the website that you do morning blood tests. "
            "How much without a referral, and when are appointments available?"
        ),
        "message_body_he": (
            "ראיתי באתר שאתם עושים בדיקות דם בבוקר. כמה זה עולה בלי הפניה ומתי יש תורים?"
        ),
        "score": 58,
        "summary_en": "Pricing and availability inquiry for blood tests without a referral.",
        "summary_he": "בירור מחיר וזמינות לבדיקות דם ללא הפניה.",
        "urgency": "Low",
        "detected_intent_en": "Lab pricing",
        "detected_intent_he": "תמחור בדיקות",
    },
]


def _pick(item: Dict[str, Any], key: str, *fallback_keys: str) -> Optional[str]:
    for k in (key, *fallback_keys):
        val = item.get(k)
        if val is not None and str(val).strip() != "":
            return str(val)
    return None


def _lead_from_seed(item: Dict[str, Any], *, live: bool = False) -> Lead:
    hours_ago = int(item.get("hours_ago", 0))
    created = datetime.now(timezone.utc) - timedelta(hours=hours_ago)

    name_en = _pick(item, "contact_name_en", "contact_name")
    name_he = _pick(item, "contact_name_he", "contact_name")
    msg_en = _pick(item, "message_body_en", "message_body") or ""
    msg_he = _pick(item, "message_body_he", "message_body") or msg_en
    sum_en = _pick(item, "summary_en", "summary") or ""
    sum_he = _pick(item, "summary_he", "summary") or sum_en
    intent_en = _pick(item, "detected_intent_en", "detected_intent") or ""
    intent_he = _pick(item, "detected_intent_he", "detected_intent") or intent_en

    # Primary columns remain populated for Streamlit / older consumers (English default).
    primary_name = name_en or name_he
    payload = {
        "source": item.get("source"),
        "channel": item.get("channel"),
        "name": primary_name,
        "name_en": name_en,
        "name_he": name_he,
        "email": item.get("contact_email"),
        "phone": item.get("contact_phone"),
        "message": msg_en or msg_he,
        "message_en": msg_en,
        "message_he": msg_he,
        "seed": not live,
        "live_demo": live,
    }
    return Lead(
        created_at=created,
        raw_payload=payload,
        source=item.get("source"),
        channel=item.get("channel"),
        contact_name=primary_name,
        contact_email=item.get("contact_email"),
        contact_phone=item.get("contact_phone"),
        message_body=msg_en or msg_he,
        score=int(item["score"]),
        summary=sum_en or sum_he,
        urgency=item["urgency"],
        detected_intent=intent_en or intent_he,
        stage=item.get("stage", "New"),
        contact_name_en=name_en,
        contact_name_he=name_he,
        message_body_en=msg_en or None,
        message_body_he=msg_he or None,
        summary_en=sum_en or None,
        summary_he=sum_he or None,
        detected_intent_en=intent_en or None,
        detected_intent_he=intent_he or None,
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
    """Insert seed leads when empty, or reseed if bilingual fields are missing."""
    count = await session.scalar(select(func.count()).select_from(Lead))
    if not count or count == 0:
        for item in SEED_LEADS:
            session.add(_lead_from_seed(item))
        await session.commit()
        return len(SEED_LEADS)

    # Upgrade pre-i18n databases so EN/HE toggle works on existing demo data.
    sample = (
        await session.execute(select(Lead).order_by(Lead.id.asc()).limit(1))
    ).scalar_one_or_none()
    if sample is not None and not sample.summary_en and not sample.summary_he:
        return await reset_and_seed(session)
    return 0


async def reset_and_seed(session: AsyncSession) -> int:
    """Delete all leads and re-insert the fictional seed set. Returns seed count."""
    await session.execute(delete(Lead))
    await session.commit()
    for item in SEED_LEADS:
        session.add(_lead_from_seed(item))
    await session.commit()
    return len(SEED_LEADS)
