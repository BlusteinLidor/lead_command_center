import os
from typing import Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI

from models import LeadAnalysis

load_dotenv()

MODEL_NAME = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a lead analyst for a sales / clinic intake team.
Analyze the lead message and return a structured assessment in BOTH English and Hebrew.

Rules:
- Score 1-100 reflects purchase intent, fit, and clarity (higher = stronger lead).
- Urgency must be exactly one of: Low, Med, High.
- Provide parallel fields in English and Hebrew for: summary, detected_intent, and message.
- summary_en / summary_he: one or two concise sentences in that language.
- detected_intent_en / detected_intent_he: a short label for what the lead wants.
- message_en / message_he: the full lead message translated accurately into each language.
  If the input is already in one of those languages, that side may match the input closely;
  still provide a faithful translation for the other language.
- contact_name_en / contact_name_he: if a contact name is provided in context, transliterate
  or keep the native form appropriately (Latin script for English, Hebrew script for Hebrew
  when the name is Hebrew). If no name is given, omit both or leave null.
- The input might be in Hebrew. Process it accurately.
- Always fill BOTH language sides — never leave Hebrew or English content blank.
"""


def _build_user_content(message: str, context: Optional[str]) -> str:
    parts = [f"Lead message:\n{message}"]
    if context and context.strip():
        parts.append(f"\nAdditional context:\n{context.strip()}")
    return "\n".join(parts)


async def analyze_lead(message: str, context: Optional[str] = None) -> LeadAnalysis:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = AsyncOpenAI(api_key=api_key)
    user_content = _build_user_content(message, context)

    response = await client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        response_format=LeadAnalysis,
    )

    choice = response.choices[0]
    parsed = choice.message.parsed
    if parsed is None:
        raise RuntimeError("OpenAI returned no parsed structured output.")
    return parsed
