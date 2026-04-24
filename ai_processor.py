import os
from typing import Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI

from models import LeadAnalysis

load_dotenv()

MODEL_NAME = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a lead analyst for a sales team.
Analyze the lead message and return a structured assessment.

Rules:
- Score 1-100 reflects purchase intent, fit, and clarity (higher = stronger lead).
- Urgency must be exactly one of: Low, Med, High.
- detected_intent: a short label for what the lead wants (e.g. pricing, demo, support).
- summary: one or two concise sentences.

The input might be in Hebrew. Process it accurately and provide the summary in the same language as the input.
If the input is Hebrew, write summary in Hebrew. If the input is English, write summary in English.
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
