import csv
from pathlib import Path
from typing import List, Dict

def catalog_path(business_id: str) -> Path:
    safe = (business_id or "default").strip()
    return Path(f"data/catalog_{safe}.csv")

def load_catalog(business_id: str) -> List[Dict[str, str]]:
    path = catalog_path(business_id)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def find_matches(query: str, catalog: List[Dict[str, str]], limit: int = 3) -> List[Dict[str, str]]:
    q = query.lower().strip()
    if not q:
        return []

    scored = []
    for row in catalog:
        hay = " ".join([
            row.get("sku",""),
            row.get("name",""),
            row.get("category",""),
            row.get("details",""),
        ]).lower()
        score = 0
        for token in q.split():
            if token in hay:
                score += 1
        if score > 0:
            scored.append((score, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:limit]]

def format_matches(matches: List[Dict[str, str]]) -> str:
    lines = []
    for m in matches:
        lines.append(
            f"- {m.get('name','').strip()} | ₹{m.get('price_inr','').strip()} | {m.get('details','').strip()}"
        )
    return "\n".join(lines)
