from typing import List, Dict, Optional
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

SYSTEM_PROMPT = (
    "You are a WhatsApp sales assistant for a business.\n\n"
    "Rules:\n"
    "- Reply short and professional (WhatsApp style)\n"
    "- If user asks price/product: use the catalog info provided (do NOT invent prices)\n"
    "- If unsure: ask 1-2 clarifying questions\n"
    "- Always try to move toward closing (booking / call / visit)\n"
    "- Output plain text only (no XML)\n"
)

def _format_catalog_context(user_message: str, business_id: str) -> str:
    catalog = load_catalog(business_id)
    matches = find_matches(user_message, catalog, limit=3)
    if not matches:
        return "No catalog matches."
    return "Catalog matches:\n" + format_matches(matches)

def generate_reply(
    user_message: str,
    status: str,
    business_id: str,
    history: Optional[List[Dict[str, str]]] = None
) -> str:
    # Booking intent: always ask for details
    if status == "BOOKING":
        return booking_reply()

    # Rule-based fallback (no OpenAI key)
    if not settings.openai_api_key:
        ctx = _format_catalog_context(user_message, business_id)
        if ctx.startswith("Catalog matches:\n"):
            cleaned = ctx.replace("Catalog matches:\n", "", 1)
            return (
                "Here are matching options:\n"
                + cleaned
                + "\n\nWhich one do you want? Share your requirement and budget."
            )
        return (
            "Please share the exact product/service name or category and your budget. "
            "I’ll share the best options."
        )

    # LLM mode
    catalog_context = _format_catalog_context(user_message, business_id)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": (
                f"Business ID: {business_id}\n"
                "Use this catalog context (do not invent items/prices):\n"
                f"{catalog_context}"
            ),
        },
    ]

    # Add memory (last N messages)
    if history:
        for h in history[-10:]:
            r = h.get("role")
            c = h.get("content")
            if r in ("user", "assistant") and c:
                messages.append({"role": r, "content": c})

    # Current message
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()
