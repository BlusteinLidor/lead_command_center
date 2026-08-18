import random
import time
import uuid

import httpx

CHANNELS = [
    "chat",
    "inbound",
    "contact_form",
    "demo_request",
    "lead_ad",
    "email_reply",
    "website_widget",
]

SOURCES = [
    "whatsapp",
    "facebook",
    "linkedin",
    "webform",
    "email",
    "partner_referral",
    "google_ads",
]

NAMES = ["Alex", "Sam", "Dana", "Noa", "Chris", "Jordan", "Maya"]
MESSAGES = [
    "Hi, I want a product demo for our team.",
    "Can someone show us a quick platform walkthrough?",
    "Interested in booking a live demo this week.",
    "Need a demo and pricing for 25 users.",
    "Please schedule a demo call for next week.",
]


def main() -> None:
    print("Demo sender started: posting every 30 seconds.")
    with httpx.Client(timeout=30) as client:
        while True:
            payload = {
                "event_id": str(uuid.uuid4()),
                "name": random.choice(NAMES),
                "message": random.choice(MESSAGES),
                "channel": random.choice(CHANNELS),
                "source": random.choice(SOURCES),
            }
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                response = client.post("http://127.0.0.1:8000/webhook/lead", json=payload)
                print(
                    f"[{timestamp}] status={response.status_code} "
                    f"channel={payload['channel']} source={payload['source']}"
                )
            except Exception as exc:
                print(f"[{timestamp}] error={exc}")
            time.sleep(30)


if __name__ == "__main__":
    main()
