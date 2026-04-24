import html
import os
import textwrap
from typing import Dict, List, Tuple

import httpx
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# Streamlit 1.40 (last release for Python 3.8) does not support row_height / in-cell wrap;
# insert soft newlines so long values render on multiple lines instead of bleeding into neighbors.
_LEAD_TEXT_WRAP_COLS = ("message_body", "summary", "detected_intent")
_LEAD_TEXT_WRAP_WIDTH = 56


def _soft_wrap_cell(value: object, width: int = _LEAD_TEXT_WRAP_WIDTH) -> object:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return value
    s = str(value)
    if not s.strip():
        return s
    return textwrap.fill(s, width=width, break_long_words=True, break_on_hyphens=False)


def _leads_display_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in _LEAD_TEXT_WRAP_COLS:
        if col in out.columns:
            out[col] = out[col].map(_soft_wrap_cell)
    return out


# Sidebar test payloads: each tuple is (short label, JSON body). All contacts and copy are unique.
HEBREW_SAMPLE_LEADS: List[Tuple[str, Dict]] = [
    (
        "דחיפות — הצעת מחיר ארגונית",
        {
            "source": "whatsapp",
            "channel": "chat",
            "name": "דני כהן",
            "phone": "+972-50-0000001",
            "message": (
                "שלום, אני צריך הצעת מחיר דחופה לפרויקט של 200 משתמשים. "
                "אפשר שיחה היום?"
            ),
        },
    ),
    (
        "בריאות — CRM למרפאה",
        {
            "source": "webform",
            "channel": "contact",
            "name": "מיכל לוי",
            "phone": "+972-52-1112233",
            "email": "michal.levi.clinic@example.co.il",
            "message": (
                "מנהלים רשת מרפאות בדרום ומחפשים CRM עם תאום תורים ותיעוד רפואי "
                "בהתאם לרגולציה. מתעניינים בהדגמה בשבוע הבא."
            ),
        },
    ),
    (
        "עסק קטן — אתר חדש",
        {
            "source": "facebook",
            "channel": "lead_ad",
            "name": "יוסי אברהם",
            "phone": "+972-54-9988776",
            "message": (
                "יש לי עסק לשיפוצים, צריך אתר פשוט עם גלריה וטופס יצירת קשר. "
                "מה המחיר וכמה זמן זה לוקח?"
            ),
        },
    ),
    (
        "עמותה — הנחה ומענק",
        {
            "source": "email",
            "channel": "inbound",
            "name": "נועה גל",
            "email": "noa.gal.nonprofit@example.org",
            "message": (
                "אנחנו עמותה לחינוך בפריפריה. האם יש מסלול מוזל או מענק ל-NGO? "
                "צריכים לעלות לאוויר לפני פתיחת שנת הלימודים."
            ),
        },
    ),
    (
        "טכנולוגיה — אינטגרציה ל-API",
        {
            "source": "linkedin",
            "channel": "message",
            "name": "עומר חדד",
            "phone": "+972-58-7766554",
            "message": (
                "מפתחים מערכת פנימית ורוצים לחבר webhook לניהול לידים. "
                "יש תיעוד ל-API וסנדבוקס לבדיקות?"
            ),
        },
    ),
    (
        "חינוך — LMS לבית ספר",
        {
            "source": "webform",
            "channel": "demo_request",
            "name": "שירה בן-עמי",
            "email": "shira.benami.school@example.edu.il",
            "message": (
                "רכזת דיגיטל בבית ספר תיכון. מעוניינים ב-LMS עם מחלקות לפי כיתות "
                "והרשאות למורים. אפשר פגישה עם צוות ה-IT שלנו?"
            ),
        },
    ),
    (
        "נמוך — תודה בלבד אחרי וובינר",
        {
            "source": "email",
            "channel": "reply",
            "name": "טל אורן",
            "email": "tal.oren.thanks@example.co.il",
            "message": (
                "היי, תודה על הוובינר אתמול, היה מעניין. לא צריך כלום נוסף כרגע."
            ),
        },
    ),
    (
        "נמוך — טעות במספר",
        {
            "source": "whatsapp",
            "channel": "chat",
            "name": "רוני פלג",
            "phone": "+972-50-4433221",
            "message": "סליחה, חשבתי שזה שיל הנהג. תתעלמו מההודעה.",
        },
    ),
    (
        "נמוך — מחפשת עבודה (לא לקוח)",
        {
            "source": "linkedin",
            "channel": "inmail",
            "name": "ליהי ברק",
            "email": "lihi.barak.cv@example.com",
            "message": (
                "ראיתי שאתם מגייסים מפתחת Full Stack. אפשר לשלוח קורות חיים "
                "למייל הזה?"
            ),
        },
    ),
    (
        "נמוך — סקרנות כללית בלי צורך עסקי",
        {
            "source": "webform",
            "channel": "generic",
            "name": "יובל סתיו",
            "phone": "+972-52-6677889",
            "message": "שמעתי את השם שלכם בפודקאסט. מה בדיוק המוצר עושה? סתם סקרן.",
        },
    ),
]

ENGLISH_SAMPLE_LEADS: List[Tuple[str, Dict]] = [
    (
        "Enterprise — demo this week",
        {
            "source": "webform",
            "channel": "landing",
            "name": "Alex Rivera",
            "email": "alex.rivera.procurement@example.com",
            "body": (
                "We are evaluating your enterprise plan for 50 seats and need "
                "a demo this week."
            ),
        },
    ),
    (
        "Startup — 90-day pilot",
        {
            "source": "producthunt",
            "channel": "referral",
            "name": "Jordan Kim",
            "email": "jordan.kim.founder@example.io",
            "body": (
                "Early-stage SaaS (12 people). Interested in a 90-day pilot with "
                "usage-based pricing and a solution engineer for onboarding."
            ),
        },
    ),
    (
        "Finance — audit & data residency",
        {
            "source": "webform",
            "channel": "security",
            "name": "Priya Sharma",
            "email": "priya.sharma.risk@example.bank",
            "body": (
                "Before procurement sign-off we need SOC2 report, data residency "
                "options in the EU, and answers on encryption at rest for attachments."
            ),
        },
    ),
    (
        "Retail — POS integration",
        {
            "source": "partner",
            "channel": "co_marketing",
            "name": "Marcus Webb",
            "phone": "+1-415-555-0192",
            "body": (
                "We run 40 stores and use Square. Do you offer a native connector or "
                "only Zapier? Need near-real-time inventory sync."
            ),
        },
    ),
    (
        "Renewal at risk — executive sponsor",
        {
            "source": "crm",
            "channel": "customer_success",
            "name": "Elena Petrov",
            "email": "elena.petrov.ops@example.corp",
            "body": (
                "Our renewal is in 30 days. Adoption in two regions is low; we need "
                "an executive business review and a concrete success plan or we churn."
            ),
        },
    ),
    (
        "Nonprofit — grant-funded rollout",
        {
            "source": "webform",
            "channel": "ngo",
            "name": "Sam Okonkwo",
            "email": "sam.okonkwo.programs@example-ngo.org",
            "body": (
                "Grant covers tooling for three years for 200 volunteers. "
                "Need invoicing that matches donor reporting and training in French."
            ),
        },
    ),
    (
        "Low score — thanks only",
        {
            "source": "email",
            "channel": "reply",
            "name": "Taylor Quinn",
            "email": "taylor.quinn.notes@example.com",
            "body": (
                "Thanks for the PDF, I skimmed it. No next steps from my side right now."
            ),
        },
    ),
    (
        "Low score — vendor pitching you",
        {
            "source": "cold_email",
            "channel": "outbound_mistake",
            "name": "Blake Foster",
            "email": "blake.foster.leadgen@example.agency",
            "body": (
                "We sell outsourced SDR services. Want 20 qualified meetings/month? "
                "Reply YES for pricing."
            ),
        },
    ),
    (
        "Low score — student paper",
        {
            "source": "webform",
            "channel": "contact",
            "name": "Nora Díaz",
            "email": "nora.diaz.mba@example.edu",
            "body": (
                "I'm writing a case study for class. Could someone answer three "
                "anonymous survey questions? No budget and not evaluating vendors."
            ),
        },
    ),
    (
        "Low score — unsubscribe",
        {
            "source": "email",
            "channel": "list",
            "name": "Chris Vale",
            "email": "chris.vale.personal@example.net",
            "body": (
                "Please remove me from all marketing lists and delete my trial data. "
                "Not interested."
            ),
        },
    ),
    (
        "Low score — are you hiring?",
        {
            "source": "webform",
            "channel": "careers_misroute",
            "name": "Morgan Liu",
            "email": "morgan.liu.jobs@example.io",
            "body": (
                "I applied on your careers page but got no reply. "
                "Is the backend role still open?"
            ),
        },
    ),
]


def fetch_leads() -> List[Dict]:
    with httpx.Client(timeout=60.0) as client:
        r = client.get(f"{API_BASE_URL}/leads")
        r.raise_for_status()
        return r.json()


def post_simulated_lead(payload: Dict) -> Tuple[bool, str]:
    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post(f"{API_BASE_URL}/webhook/lead", json=payload)
            if r.status_code == 201:
                return True, "Lead ingested successfully."
            return False, "{0}: {1}".format(r.status_code, r.text)
    except httpx.RequestError as e:
        return False, "Request failed: {0!s}".format(e)


def main() -> None:
    st.set_page_config(page_title="Lead Command Center", layout="wide")

    st.markdown(
        """
<style>
.hebrew-cell {
  direction: rtl;
  text-align: right;
  unicode-bidi: plaintext;
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.title("Lead Command Center")
    st.caption("Ingestion via FastAPI · AI scoring · SQLite persistence")

    with st.sidebar:
        st.header("Simulate lead")
        lang = st.radio("Sample language", ("Hebrew", "English"), horizontal=True)
        scenarios = HEBREW_SAMPLE_LEADS if lang == "Hebrew" else ENGLISH_SAMPLE_LEADS
        labels = [label for label, _ in scenarios]
        choice = st.selectbox("Scenario", labels, index=0)
        sample = dict(next(payload for lab, payload in scenarios if lab == choice))
        if st.button("Send test JSON to webhook", type="primary"):
            ok, msg = post_simulated_lead(sample)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

        st.divider()
        st.text_input(
            "API base URL",
            value=API_BASE_URL,
            disabled=True,
            help="Set API_BASE_URL in .env",
        )

    try:
        leads = fetch_leads()
    except httpx.HTTPStatusError as e:
        st.error("Could not load leads: {0!s}".format(e))
        return
    except httpx.RequestError as e:
        st.error(
            "Could not reach API at {0}. Start the server with: "
            "`uvicorn main:app --reload --host 127.0.0.1 --port 8000` — {1!s}".format(
                API_BASE_URL,
                e,
            )
        )
        return

    total = len(leads)
    high_urgency = sum(1 for x in leads if x.get("urgency") == "High")
    avg_score = (
        round(sum(x.get("score", 0) for x in leads) / total, 1) if total else 0.0
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total leads", total)
    c2.metric("High urgency leads", high_urgency)
    c3.metric("Average lead score", "{0:.1f}".format(avg_score))

    st.subheader("All leads")

    if not leads:
        st.info("No leads yet. Use **Simulate lead** in the sidebar.")
        return

    df = pd.DataFrame(leads)
    display_cols = [
        "id",
        "created_at",
        "source",
        "channel",
        "contact_name",
        "message_body",
        "score",
        "urgency",
        "detected_intent",
        "summary",
    ]
    for col in display_cols:
        if col not in df.columns:
            df[col] = None
    df = df[display_cols]
    display_df = _leads_display_dataframe(df)

    lead_column_config = {
        "id": st.column_config.NumberColumn("ID", format="%d", width="small"),
        "created_at": st.column_config.TextColumn("Created", width="medium"),
        "source": st.column_config.TextColumn("Source", width="small"),
        "channel": st.column_config.TextColumn("Channel", width="small"),
        "contact_name": st.column_config.TextColumn("Contact", width="medium"),
        "message_body": st.column_config.TextColumn("Message", width="large"),
        "score": st.column_config.NumberColumn("Score", format="%.1f", width="small"),
        "urgency": st.column_config.TextColumn("Urgency", width="small"),
        "detected_intent": st.column_config.TextColumn("Intent", width="medium"),
        "summary": st.column_config.TextColumn("Summary", width="large"),
    }

    try:
        styled = display_df.style.set_properties(
            subset=["summary"],
            **{"classes": "hebrew-cell"},
        )
        st.dataframe(
            styled,
            column_config=lead_column_config,
            use_container_width=True,
            hide_index=True,
            height=640,
        )
    except Exception:
        st.dataframe(
            display_df,
            column_config=lead_column_config,
            use_container_width=True,
            hide_index=True,
            height=640,
        )

    with st.expander("Summaries (RTL-safe view)"):
        for row in leads:
            sid = html.escape(str(row.get("id", "")))
            s = row.get("summary") or ""
            safe = html.escape(s)
            st.markdown(
                '<p><strong>#{0}</strong></p><div class="hebrew-cell">{1}</div>'.format(
                    sid, safe
                ),
                unsafe_allow_html=True,
            )


main()
