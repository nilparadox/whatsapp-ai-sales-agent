from openai import OpenAI
from app.core.config import settings
from app.services.catalog_service import load_catalog, find_matches, format_matches

client = OpenAI(api_key=settings.openai_api_key)

def booking_reply() -> str:
    return (
        "Great — to confirm your booking, please share:\n"
        "1) Your name\n"
        "2) Delivery/installation address (area + pin)\n"
        "3) Preferred date & time\n"
        "4) Phone number for confirmation\n"
        "I’ll schedule it for you."
    )

SYSTEM_PROMPT = """
You are a WhatsApp sales assistant for a business.

Rules:
- Reply short and professional (WhatsApp style)
- If user asks price/product: use the catalog info provided (do NOT invent prices)
- If unsure: ask 1-2 clarifying questions
- Always try to move toward closing (booking / call / visit)
- Output plain text only (no XML)
"""

def generate_reply(user_message: str, status: str, business_id: str) -> str:
    if status == "BOOKING":
        return booking_reply()

    catalog = load_catalog(business_id)
    matches = find_matches(user_message, catalog, limit=3)

    # No API key → still sellable demo, but business-specific
    if not settings.openai_api_key:
        if matches:
            return (
                "Here are matching options:\n"
                f"{format_matches(matches)}\n\n"
                "Which one do you want? Share your requirement and budget."
            )
        return (
            "Please share the exact product/service name or category and your budget. "
            "I’ll share the best options."
        )

    catalog_context = "No catalog matches." if not matches else f"Catalog matches:\n{format_matches(matches)}"

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Business ID: {business_id}\nUse this catalog context:\n{catalog_context}"},
            {"role": "user", "content": user_message}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
