import html
import os
import textwrap
import threading
import time
from typing import Dict, List, Optional, Tuple

import httpx
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
EMBED_PORT = int(os.getenv("DEMO_API_PORT", "8000"))

# Streamlit 1.40 (last release for Python 3.8) does not support row_height / in-cell wrap;
# insert soft newlines so long values render on multiple lines instead of bleeding into neighbors.
_LEAD_TEXT_WRAP_COLS = ("message_body", "summary", "detected_intent")
_LEAD_TEXT_WRAP_WIDTH = 56

LEAD_STAGES = ("New", "Contacted", "Qualified", "Closed")


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


def _should_embed_api() -> bool:
    flag = os.getenv("DEMO_EMBED_API", "").strip().lower()
    if flag in ("1", "true", "yes"):
        return True
    if flag in ("0", "false", "no"):
        return False
    # Default: embed on Streamlit Cloud, or when pointing at local API.
    if os.path.exists("/mount/src"):
        return True
    return "127.0.0.1" in API_BASE_URL or "localhost" in API_BASE_URL


def _api_healthy(base: Optional[str] = None) -> bool:
    url = (base or API_BASE_URL).rstrip("/") + "/health"
    try:
        with httpx.Client(timeout=1.5) as client:
            r = client.get(url)
            return r.status_code == 200
    except Exception:
        return False


def _run_embedded_api(host: str, port: int) -> None:
    import uvicorn

    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            log_level="warning",
            access_log=False,
        )
    except OSError:
        # Port already in use — assume an API is already running.
        pass


@st.cache_resource
def bootstrap_backend() -> str:
    """Optionally start FastAPI in-process (Streamlit Cloud / single-process demo)."""
    if not _should_embed_api():
        return "external"

    if _api_healthy():
        return "already-running"

    host = "127.0.0.1"
    thread = threading.Thread(
        target=_run_embedded_api,
        args=(host, EMBED_PORT),
        daemon=True,
        name="lead-command-api",
    )
    thread.start()

    deadline = time.time() + 15.0
    while time.time() < deadline:
        if _api_healthy():
            return "embedded"
        time.sleep(0.15)
    return "embed-timeout"


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
]

ENGLISH_SAMPLE_LEADS: List[Tuple[str, Dict]] = [
    (
        "Urgent — enterprise quote today",
        {
            "source": "whatsapp",
            "channel": "chat",
            "name": "Dana Cole",
            "phone": "+1-415-555-0101",
            "body": (
                "Hi, I need an urgent quote for a 200-user rollout. "
                "Can we talk today?"
            ),
        },
    ),
    (
        "Healthcare — clinic CRM demo",
        {
            "source": "webform",
            "channel": "contact",
            "name": "Maya Stern",
            "phone": "+1-628-555-0144",
            "email": "maya.stern.clinic@example.com",
            "body": (
                "We run a small clinic network and need CRM with appointment "
                "scheduling and chart notes. Interested in a demo next week."
            ),
        },
    ),
    (
        "SMB — new marketing site",
        {
            "source": "facebook",
            "channel": "lead_ad",
            "name": "Joe Abrams",
            "phone": "+1-347-555-0199",
            "body": (
                "I have a remodeling business and need a simple site with a gallery "
                "and contact form. What's the price and timeline?"
            ),
        },
    ),
    (
        "Nonprofit — discount / grant",
        {
            "source": "email",
            "channel": "inbound",
            "name": "Nina Gale",
            "email": "nina.gale.nonprofit@example.org",
            "body": (
                "We're an education nonprofit. Is there a discounted plan or grant "
                "for NGOs? We need to launch before the school year."
            ),
        },
    ),
    (
        "Tech — webhook / API sandbox",
        {
            "source": "linkedin",
            "channel": "message",
            "name": "Omar Haddad",
            "phone": "+1-646-555-0177",
            "body": (
                "We're building an internal system and want to connect a lead "
                "webhook. Do you have API docs and a sandbox?"
            ),
        },
    ),
    (
        "Education — school LMS",
        {
            "source": "webform",
            "channel": "demo_request",
            "name": "Sara Benami",
            "email": "sara.benami.school@example.edu",
            "body": (
                "Digital coordinator at a high school. Looking for an LMS with "
                "class cohorts and teacher permissions. Can we meet our IT team?"
            ),
        },
    ),
    (
        "Low score — thanks only",
        {
            "source": "email",
            "channel": "reply",
            "name": "Alex Oran",
            "email": "alex.oran.thanks@example.com",
            "body": "Thanks for yesterday's webinar — interesting, but nothing needed now.",
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


def patch_lead_stage(lead_id: int, stage: str) -> Tuple[bool, str]:
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.patch(
                f"{API_BASE_URL}/leads/{lead_id}/stage",
                json={"stage": stage},
            )
            if r.status_code == 200:
                return True, "Stage updated."
            return False, "{0}: {1}".format(r.status_code, r.text)
    except httpx.RequestError as e:
        return False, "Request failed: {0!s}".format(e)


def reset_demo_data() -> Tuple[bool, str]:
    try:
        with httpx.Client(timeout=30.0) as client:
            r = client.post(f"{API_BASE_URL}/demo/reset")
            if r.status_code == 200:
                data = r.json()
                return True, "Demo reset — {0} seeded leads.".format(data.get("seeded", "?"))
            return False, "{0}: {1}".format(r.status_code, r.text)
    except httpx.RequestError as e:
        return False, "Request failed: {0!s}".format(e)


def main() -> None:
    st.set_page_config(page_title="Lead Command Center", layout="wide")

    boot = bootstrap_backend()

    st.markdown(
        """
<style>
.hebrew-cell {
  direction: rtl;
  text-align: right;
  unicode-bidi: plaintext;
}
.demo-banner {
  background: #eef3f8;
  border: 1px solid #c5d4e4;
  border-radius: 6px;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
}
.demo-banner strong { font-size: 1.05rem; }
.demo-banner .he {
  direction: rtl;
  text-align: right;
  margin-top: 0.25rem;
  color: #334;
  font-size: 0.95rem;
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="demo-banner">
  <strong>Portfolio demo — sample data only.</strong>
  <div class="he">הדגמת תיק עבודות — נתוני דמה בלבד.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.title("Lead Command Center")
    st.caption(
        "Ops board for inbound leads · AI score & summary · triage by stage "
        "(Almond Family Clinic sample)"
    )

    with st.sidebar:
        st.header("Demo controls")
        if st.button("Reset demo data", help="Restore the fictional seed leads"):
            ok, msg = reset_demo_data()
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

        st.divider()
        st.header("Simulate lead")
        st.caption("Optional — needs OPENAI_API_KEY for live AI scoring.")
        lang = st.radio("Sample language", ("Hebrew", "English"), horizontal=True)
        scenarios = HEBREW_SAMPLE_LEADS if lang == "Hebrew" else ENGLISH_SAMPLE_LEADS
        labels = [label for label, _ in scenarios]
        choice = st.selectbox("Scenario", labels, index=0)
        sample = dict(next(payload for lab, payload in scenarios if lab == choice))
        if st.button("Send test JSON to webhook", type="secondary"):
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
            help="Set API_BASE_URL in .env or Streamlit secrets",
        )
        st.caption("Backend: {0}".format(boot))

    try:
        leads = fetch_leads()
    except httpx.HTTPStatusError as e:
        st.error("Could not load leads: {0!s}".format(e))
        return
    except httpx.RequestError as e:
        st.error(
            "Could not reach API at {0}. Start the server with: "
            "`uvicorn main:app --reload --host 127.0.0.1 --port 8000` "
            "or set DEMO_EMBED_API=1 — {1!s}".format(
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
    by_stage = {s: sum(1 for x in leads if x.get("stage") == s) for s in LEAD_STAGES}

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total leads", total)
    c2.metric("High urgency", high_urgency)
    c3.metric("Average score", "{0:.1f}".format(avg_score))
    c4.metric("New / open", by_stage.get("New", 0))

    st.subheader("Triage a lead")
    st.caption("Pick a lead, change its stage, and watch the board update — the ops moment.")

    if not leads:
        st.info("No leads yet. Use **Reset demo data** in the sidebar.")
        return

    lead_options = {
        "#{0} — {1} [{2}]".format(
            row.get("id"),
            row.get("contact_name") or "Unknown",
            row.get("stage") or "New",
        ): row
        for row in leads
    }
    selected_label = st.selectbox("Lead", list(lead_options.keys()), index=0)
    selected = lead_options[selected_label]
    current_stage = selected.get("stage") or "New"
    try:
        stage_index = LEAD_STAGES.index(current_stage)
    except ValueError:
        stage_index = 0

    col_a, col_b = st.columns([2, 1])
    with col_a:
        new_stage = st.selectbox("New stage", LEAD_STAGES, index=stage_index)
    with col_b:
        st.write("")
        st.write("")
        if st.button("Update stage", type="primary", use_container_width=True):
            ok, msg = patch_lead_stage(int(selected["id"]), new_stage)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    stage_cols = st.columns(len(LEAD_STAGES))
    for col, stage in zip(stage_cols, LEAD_STAGES):
        col.metric(stage, by_stage.get(stage, 0))

    st.subheader("All leads")

    df = pd.DataFrame(leads)
    display_cols = [
        "id",
        "created_at",
        "stage",
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
        "stage": st.column_config.TextColumn("Stage", width="small"),
        "source": st.column_config.TextColumn("Source", width="small"),
        "channel": st.column_config.TextColumn("Channel", width="small"),
        "contact_name": st.column_config.TextColumn("Contact", width="medium"),
        "message_body": st.column_config.TextColumn("Message", width="large"),
        "score": st.column_config.NumberColumn("Score", format="%d", width="small"),
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
            stage = html.escape(str(row.get("stage") or ""))
            s = row.get("summary") or ""
            safe = html.escape(s)
            st.markdown(
                '<p><strong>#{0}</strong> · {1}</p>'
                '<div class="hebrew-cell">{2}</div>'.format(sid, stage, safe),
                unsafe_allow_html=True,
            )


main()
